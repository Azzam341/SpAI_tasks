from pdf2image import convert_from_path

POPPLER_PATH = r"C:\poppler-25.12.0\Library\bin"

def load_pdf_pages(pdf_path):
    pages = convert_from_path(
        pdf_path,
        poppler_path=POPPLER_PATH
    )
    return pages