import pytesseract


def ocr_image(image):
    """
    Runs OCR on a PIL image
    """

    text = pytesseract.image_to_string(image)

    return text