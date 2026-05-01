import os
from datetime import datetime

from src.agents.triage_agent import classify_page
from src.ocr.tesseract_ocr import ocr_image
from src.utils.pdf_loader import load_pdf_pages
from src.vlm.gemini_vlm_v2 import run_vlm

from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

api_key = os.getenv("GEMINI_API_KEY")

if api_key:
    print("API Key loaded successfully!")
else:
    print("API Key not found. Check your .env file and variable name.")


# -------------------------
# LOGGING SETUP
# -------------------------
def create_log_file(pdf_path):
    os.makedirs("logs", exist_ok=True)

    file_name = os.path.basename(pdf_path).replace(".pdf", "")
    log_path = f"logs/log_{file_name}.txt"

    log_file = open(log_path, "w", encoding="utf-8")

    log_file.write("====================================\n")
    log_file.write("PIPELINE LOG\n")
    log_file.write(f"FILE: {file_name}\n")
    log_file.write(f"TIME: {datetime.now()}\n")
    log_file.write("====================================\n\n")

    return log_file


def write_page_block(log_file, page_number, page_type, confidence,
                     text_length, extracted_text, final_output, route):

    log_file.write(f"\n--- PAGE {page_number} ---\n")
    log_file.write(f"PAGE_TYPE: {page_type}\n")
    log_file.write(f"CONFIDENCE: {confidence:.4f}\n")
    log_file.write(f"OCR_TEXT_LENGTH: {text_length}\n")
    log_file.write(f"ROUTE: {route}\n")

    log_file.write("\n----- EXTRACTED TEXT START -----\n")
    log_file.write(extracted_text if extracted_text else "[EMPTY TEXT]")
    log_file.write("\n----- EXTRACTED TEXT END -----\n")

    log_file.write("\n----- FINAL OUTPUT START -----\n")

    page_output = next(
        (p for p in final_output if p["page_number"] == page_number),
        None
    )

    if page_output:
        log_file.write(str(page_output["content"]))
    else:
        log_file.write("[NO OUTPUT FOUND]")

    log_file.write("\n----- FINAL OUTPUT END -----\n")
    log_file.write("------------------------------------\n")


# -------------------------
# PIPELINE
# -------------------------
def run_pipeline(pdf_path):

    print("\nStarting Pipeline...")
    print(f"📄 PDF: {pdf_path}\n")

    log_file = create_log_file(pdf_path)

    pages = load_pdf_pages(pdf_path)

    print(f"Total Pages Found: {len(pages)}\n")

    final_output = []

    for i, page_image in enumerate(pages):

        page_number = i + 1

        print("\n==============================")
        print(f"Processing Page {page_number}")
        print("==============================")

        # -------------------------
        # STEP 1: OCR
        # -------------------------
        print("🔍 Running OCR...")

        extracted_text = ocr_image(page_image)
        text_length = len(extracted_text.strip())
        text_coverage = text_length / 2000

        print(f"OCR Text Length: {text_length}")

        # -------------------------
        # STEP 2: TRIAGE
        # -------------------------
        print("Running Triage Agent...")

        result = classify_page(
            page_number=page_number,
            text=extracted_text,
            text_coverage=text_coverage
        )

        page_type = result["page_type"]
        confidence = result["confidence"]

        print(f"Page Type: {page_type}")
        print(f"Confidence: {confidence:.2f}")

        # -------------------------
        # STEP 3: ROUTING
        # -------------------------
        print("Routing Page...")

        extraction_path = ""

        if page_type == "BLUE_SLIP":
            print("🟦 BLUE SLIP detected")

            content = {
                "note": "BLUE_SLIP detected",
                "text": extracted_text
            }
            route = "BLUE_SLIP"

        elif page_type == "DIGITAL":
            print("DIGITAL page → OCR text")

            content = extracted_text
            route = "DIGITAL"

        elif page_type == "SCANNED":
            print("SCANNED page → VLM")
            #If you decide to send request to vlm, this is the logic although free credits will run out after 20 tries
            #vlm_result = run_vlm(page_image)

            #if isinstance(vlm_result, dict) and "error" in vlm_result:
            #    print("⚠️ VLM failed → fallback to OCR")
            #    content = extracted_text
            #    route = "SCANNED_FALLBACK_OCR"
            #else:
            #    content = vlm_result
            #    route = "SCANNED_VLM"

        else:
            print("Unknown type → fallback OCR")

            content = extracted_text
            route = "UNKNOWN"

        # -------------------------
        # STORE OUTPUT
        # -------------------------
        final_output.append({
            "page_number": page_number,
            "page_type": page_type,
            "content": content
        })

        # -------------------------
        # PAGE LOG BLOCK (FULL DEBUG)
        # -------------------------
        write_page_block(
            log_file=log_file,
            page_number=page_number,
            page_type=page_type,
            confidence=confidence,
            text_length=text_length,
            extracted_text=extracted_text,
            final_output=final_output,
            route=route
        )

        print("Log written")

    # -------------------------
    # END LOG
    # -------------------------
    log_file.write("\n====================================\n")
    log_file.write("PIPELINE COMPLETED\n")
    log_file.close()

    print("\n✅ Pipeline Completed Successfully\n")

    return {
        "pages": final_output
    }


# -------------------------
# ENTRY POINT
# -------------------------
if __name__ == "__main__":

    pdf_path = "data/samples/2014LHC4829.pdf"

    result = run_pipeline(pdf_path)