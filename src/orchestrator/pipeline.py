import os
from datetime import datetime

from src.agents.triage_agent import classify_page
from src.ocr.tesseract_ocr import ocr_image
from src.utils.pdf_loader import load_pdf_pages
from src.orchestrator.blue_slip_methods import build_blue_slip_metadata

from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

api_key = os.getenv("GEMINI_API_KEY")

if api_key:
    print("API Key loaded successfully!")
else:
    print("API Key not found. Check your .env file and variable name.")


# LOGGING SETUP

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


# PIPELINE

def run_pipeline(pdf_path):

    print("\nStarting Pipeline...")
    print(f" PDF: {pdf_path}\n")

    log_file = create_log_file(pdf_path)

    pages = load_pdf_pages(pdf_path)

    print(f"Total Pages Found: {len(pages)}\n")

    final_output = []


    # METADATA
    
    metadata = {
        "case_number": None,
        "decision_date": None,
        "has_blue_slip": False,
        "page_offset": 0
    }

    # BLUE SLIP CHECK (PAGE 1 ONLY)

    first_page_text = ocr_image(pages[0])

    blue_slip_meta = build_blue_slip_metadata(first_page_text)
    metadata.update(blue_slip_meta)

    if metadata["has_blue_slip"]:
        metadata["page_offset"] = 1
        print("\n BLUE SLIP DETECTED (GLOBAL METADATA SET)")
        print(metadata)

    # PAGE LOOP

    for i, page_image in enumerate(pages):

        page_number = i + 1

        print("\n==============================")
        print(f"Processing Page {page_number}")
        print("==============================")

        # STEP 1: OCR

        print("🔍 Running OCR...")

        extracted_text = ocr_image(page_image)
        text_length = len(extracted_text.strip())
        text_coverage = text_length / 2000

        print(f"OCR Text Length: {text_length}")

        # STEP 2: TRIAGE

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

        # STEP 3: ROUTING
        
        print("Routing Page...")

        route = ""

        if page_type == "BLUE_SLIP":
            print("BLUE SLIP page (ignored in content output)")

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
            print("SCANNED page → VLM (disabled for now)")
            
            # PLEASE READ THIS!
            
            #If you decide to send request to vlm, this is the logic although free credits will run out after 20 tries
            #Also note i am having quite some issues with gemini. It works on some, and completely falls flat on other files
            #Will try open router instead
            
            # vlm_result = run_vlm(page_image)

            # if isinstance(vlm_result, dict) and "error" in vlm_result:
            #     content = extracted_text
            #     route = "SCANNED_FALLBACK_OCR"
            # else:
            #     content = vlm_result
            #     route = "SCANNED_VLM"

            content = extracted_text
            route = "SCANNED_OCR_ONLY"

        else:
            print("Unknown type → fallback OCR")

            content = extracted_text
            route = "UNKNOWN"


        # STORE OUTPUT
    
        
        final_output.append({
            "page_number": page_number,
            "page_type": page_type,
            "content": content
        })

        # LOGGING

        log_file.write("\n====================================\n")
        log_file.write(f"PAGE {page_number} SUMMARY\n")
        log_file.write("====================================\n")
        log_file.write("| page_number | page_type | classified_by | confidence |\n")
        log_file.write("|-------------|-----------|---------------|------------|\n")
        log_file.write(f"| {page_number} | {page_type} | TRIAGE_AGENT | {confidence:.4f} |\n")
        log_file.write("====================================\n")
        

        #log_file.write("\n----- EXTRACTED TEXT START -----\n")
        #log_file.write(extracted_text)
        #log_file.write("\n----- EXTRACTED TEXT END -----\n")

        log_file.write("------------------------------------\n")

        print("Log written")

    # FINAL OUTPUT
    
    log_file.write("\n====================================\n")
    log_file.write("PIPELINE COMPLETED\n")
    log_file.write(f"METADATA:\n{metadata}\n")

    log_file.close()

    print("\n Pipeline Completed Successfully\n")

    return {
        "pages": final_output,
        "metadata": metadata
    }


# ENTRY POINT

if __name__ == "__main__":

    from tkinter import Tk
    from tkinter.filedialog import askopenfilename

    # hide root window
    Tk().withdraw()

    # open file browser
    pdf_path = askopenfilename(
        title="Select PDF file",
        filetypes=[("PDF Files", "*.pdf")]
    )

    if pdf_path:
        result = run_pipeline(pdf_path)
    else:
        print("No file selected.")