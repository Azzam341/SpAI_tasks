# Specter AI – Document Processing Pipeline

This project is part of the Specter Final Year Project (FYP) group. It is a document processing system designed to extract structured information from PDF files using OCR, rule-based classification, and vision-language models (VLMs).

The system handles both digital and scanned documents and routes them through appropriate extraction paths to ensure accurate data retrieval.

---

## Features

- PDF page extraction and processing
- OCR-based text extraction (Tesseract)
- Page classification using a triage agent
- Routing system for:
  - Digital pages (OCR text)
  - Scanned pages (VLM / fallback OCR)
  - Special document types (e.g., Blue Slip)
- Metadata extraction (case number, decision date)
- Structured logging per page
- File-based output for analysis and debugging

---

## Project Structure

```
src/
│
├── agents/            # Page classification logic (triage agent)
├── ocr/               # OCR implementation (Tesseract)
├── vlm/               # Vision-Language Model integration
├── utils/             # PDF loading and helpers
├── orchestrator/      # Main pipeline and workflow
│
logs/                  # Generated logs
data/samples/          # Sample PDFs
venv/                  # Virtual environment (ignored)
```

---

## How It Works

1. Load PDF and split into pages  
2. Run OCR on each page  
3. Classify page type using triage agent  
4. Route page based on type:
   - **DIGITAL** → use OCR text
   - **SCANNED** → send to VLM (or fallback OCR)
   - **BLUE_SLIP** → extract metadata + ignore in final output  
5. Store structured output and logs  

---

## Installation

```bash
git clone <repo-url>
cd Specter_AI

python -m venv venv
venv\Scripts\activate   # Windows

pip install -r requirements.txt
```

---

## Environment Variables

Create a `.env` file:

```
GEMINI_API_KEY=your_api_key_here
```

---

## Running the Pipeline

```bash
python -m src.orchestrator.pipeline
```

You will be prompted to select a PDF file.

---

## Output

- Structured page-wise JSON output
- Detailed logs in `logs/`
- Extracted metadata (if Blue Slip is detected)

---

## Notes

- VLM (Gemini) is optional and may be rate-limited
- OCR is used as fallback for reliability
- Designed for experimentation and learning purposes in document AI

---

## Purpose

This project is built for learning and experimentation within the Specter FYP group, focusing on:

- OCR systems
- Document intelligence pipelines
- AI-based page classification
- Multimodal model integration

---

## License

For educational use only.
```
