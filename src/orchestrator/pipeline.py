import os
from datetime import datetime

from src.agents.triage_agent import classify_page
from src.ocr.tesseract_ocr import ocr_image
from src.utils.pdf_loader import load_pdf_pages


# -------------------------
# LOGGING SETUP
# -------------------------
def create_log_file(pdf_path):
    os.makedirs("logs", exist_ok=True)

    file_name = os.path.basename(pdf_path).replace(".pdf", "")
    log_path = f"logs/log_{file_name}.txt"

    log_file = open(log_path, "w", encoding="utf-8")

    log_file.write("====================================\n")
    log_file.write(f"PIPELINE LOG\n")
    log_file.write(f"FILE: {file_name}\n")
    log_file.write(f"TIME: {datetime.now()}\n")
    log_file.write("====================================\n\n")

    return log_file


# -------------------------
# PIPELINE
# -------------------------
def run_pipeline(pdf_path):

    print("\n🚀 Starting Pipeline...")
    print(f"📄 PDF: {pdf_path}\n")

    log_file = create_log_file(pdf_path)

    pages = load_pdf_pages(pdf_path)

    print(f"📑 Total Pages Found: {len(pages)}\n")

    final_output = []

    for i, page_image in enumerate(pages):

        page_number = i + 1

        print(f"\n==============================")
        print(f"📄 Processing Page {page_number}")
        print(f"==============================")

        log_file.write(f"\n--- PAGE {page_number} ---\n")

        # -------------------------
        # STEP 1: OCR
        # -------------------------
        print("🔍 Running OCR...")

        extracted_text = ocr_image(page_image)

        text_length = len(extracted_text.strip())
        text_coverage = text_length / 2000

        print(f"📝 OCR Text Length: {text_length}")

        log_file.write(f"OCR_TEXT_LENGTH: {text_length}\n")

        # -------------------------
        # STEP 2: TRIAGE
        # -------------------------
        print("🧠 Running Triage Agent...")

        result = classify_page(
            page_number=page_number,
            text=extracted_text,
            text_coverage=text_coverage
        )

        page_type = result["page_type"]
        confidence = result["confidence"]

        print(f"🏷️ Page Type: {page_type}")
        print(f"🎯 Confidence: {confidence:.2f}")

        log_file.write(f"PAGE_TYPE: {page_type}\n")
        log_file.write(f"CONFIDENCE: {confidence:.4f}\n")

        # -------------------------
        # STEP 3: ROUTING
        # -------------------------
        print("📦 Routing Page...")

        if page_type == "BLUE_SLIP":
            print("🟦 BLUE SLIP detected")

            content = {
                "note": "BLUE_SLIP detected",
                "text": extracted_text
            }

            log_file.write("ROUTE: BLUE_SLIP\n")

        elif page_type == "DIGITAL":
            print("🟩 DIGITAL page → OCR text")

            content = extracted_text

            log_file.write("ROUTE: DIGITAL\n")

        elif page_type == "SCANNED":
            print("🟨 SCANNED page → OCR (VLM later)")

            content = extracted_text

            log_file.write("ROUTE: SCANNED\n")

        else:
            print("⚠️ Unknown type → fallback OCR")

            content = extracted_text

            log_file.write("ROUTE: UNKNOWN\n")

        final_output.append({
            "page_number": page_number,
            "page_type": page_type,
            "content": content
        })

        log_file.write(f"TEXT_LENGTH: {text_length}\n")
        log_file.write("------------------------------------\n")

        print("📊 Log written")

    log_file.write("\n====================================\n")
    log_file.write("PIPELINE COMPLETED\n")
    log_file.close()

    print("\n✅ Pipeline Completed Successfully\n")

    return {
    }


# -------------------------
# ENTRY POINT
# -------------------------
if __name__ == "__main__":

    pdf_path = "data/samples/dummy/2025LHC495.pdf"

    result = run_pipeline(pdf_path)