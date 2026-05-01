Description

This project is a PDF document processing system built for the Specter FYP group. It is designed to extract structured information from PDF files using a combination
of OCR, rule based classification, and vision language models for image based pages. The system identifies different types of pages such as digital text pages, 
scanned image pages, and special Blue Slip pages. It then routes each page through the appropriate processing path and produces structured output along with detailed 
logs and metadata. The main goal of this project is to learn and demonstrate how real world document understanding systems are built using a pipeline based architecture combining classical OCR techniques and modern AI models.

File Structure

src contains all source code
src orchestrator contains the main pipeline and workflow logic
src agents contains the triage agent used for page classification
src ocr contains OCR implementation using Tesseract
src vlm contains vision language model integration
src utils contains helper functions such as PDF loading
data samples contains input PDF files for testing
logs stores generated pipeline logs
venv is the Python virtual environment
requirements txt contains all dependencies
