import re


def is_blue_slip(text: str) -> bool:
    """
    Detects whether a page is a Blue Slip page.
    """
    text_lower = text.lower()
    return ("blue slip" in text_lower) or ("hjd/c" in text_lower)


def extract_case_and_date(text: str):
    """
    Extracts case number and decision date using regex.
    (baseline version, can be improved later with VLM/LLM)
    """

    case_number = None
    decision_date = None

    case_patterns = [
        r"\b\d{4}[A-Z]{2,5}\d+\b",   # 2024LHC1234
        r"\b\d{1,5}/\d{4}\b"         # 123/2024
    ]

    date_patterns = [
        r"\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b",
        r"\b\d{1,2}\s+(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+\d{2,4}\b"
    ]

    for p in case_patterns:
        match = re.search(p, text)
        if match:
            case_number = match.group(0)
            break

    for p in date_patterns:
        match = re.search(p, text, re.IGNORECASE)
        if match:
            decision_date = match.group(0)
            break

    return case_number, decision_date


def build_blue_slip_metadata(text: str):
    """
    High-level helper: detects + extracts + returns structured metadata.
    """

    if not is_blue_slip(text):
        return {
            "has_blue_slip": False,
            "case_number": None,
            "decision_date": None,
        }

    case_number, decision_date = extract_case_and_date(text)

    return {
        "has_blue_slip": True,
        "case_number": case_number,
        "decision_date": decision_date,
    }