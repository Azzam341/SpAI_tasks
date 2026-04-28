from src.agents.triage_agent import classify_page
from src.ocr.tesseract_ocr import ocr_image
from src.utils.pdf_loader import load_pdf_pages


def run_pipeline(pdf_path):

    print("\n🚀 Starting Pipeline...")
    print(f"📄 PDF: {pdf_path}\n")

    pages = load_pdf_pages(pdf_path)

    print(f"📑 Total Pages Found: {len(pages)}\n")

    final_output = []
    logs = []

    for i, page_image in enumerate(pages):

        page_number = i + 1

        print(f"\n==============================")
        print(f"📄 Processing Page {page_number}")
        print(f"==============================")

        # -------------------------
        # STEP 1: OCR
        # -------------------------
        print("🔍 Running OCR...")

        extracted_text = ocr_image(page_image)

        text_length = len(extracted_text.strip())

        print(f"📝 OCR Text Length: {text_length}")

        # simple heuristic for now
        text_coverage = text_length / 2000

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

        # -------------------------
        # STEP 3: ROUTING
        # -------------------------
        print("📦 Routing Page...")

        if page_type == "BLUE_SLIP":
            print("🟦 BLUE SLIP detected (placeholder handling)")

            content = {
                "note": "BLUE_SLIP detected",
                "text": extracted_text
            }

        elif page_type == "DIGITAL":
            print("🟩 DIGITAL page → using OCR text")

            content = extracted_text

        elif page_type == "SCANNED":
            print("🟨 SCANNED page → using OCR (VLM not added yet)")

            content = extracted_text

        else:
            print("⚠️ Unknown type → defaulting to OCR text")

            content = extracted_text

        final_output.append({
            "page_number": page_number,
            "page_type": page_type,
            "content": content
        })

        # -------------------------
        # STEP 4: LOGGING
        # -------------------------
        log_entry = {
            "page_number": page_number,
            "page_type": page_type,
            "confidence": confidence,
            "text_length": text_length
        }

        logs.append(log_entry)

        print("📊 Log stored")

    print("\n✅ Pipeline Completed Successfully\n")

    return {
        "pages": final_output,
        "logs": logs
    }
    
if __name__ == "__main__":

    pdf_path = "data/samples/dummy/2024LHC4594 (3).pdf"

    result = run_pipeline(pdf_path)

    print("\n📦 FINAL OUTPUT")
    print(result)