# src/agents/triage_agent.py

def classify_page(page_number: int,
                  text: str,
                  text_coverage: float):

    text_lower = text.lower()

    # ----------------------------
    # 1. BLUE SLIP OVERRIDE RULE
    # ----------------------------
    if page_number == 1:
        if "blue slip" in text_lower or "hjd/c" in text_lower:
            return {
                "page_type": "BLUE_SLIP",
                "confidence": 0.99,
                "reason": "Blue Slip detected on page 1"
            }

    # ----------------------------
    # 2. DIGITAL PAGE RULE
    # ----------------------------
    if text_coverage >= 0.6:
        return {
            "page_type": "DIGITAL",
            "confidence": min(0.95, 0.7 + text_coverage * 0.3),
            # 0.7 is selected as a baseline, we give it a small bonus to smoothly boost/decrease confidence, capped at 0.95 to prevent
            #over-confident decisions
            "reason": "Text coverage above threshold"
        }

    # ----------------------------
    # 3. SCANNED PAGE RULE
    # ----------------------------
    return {
        "page_type": "SCANNED",
        "confidence": 0.8,
        "reason": "Low text coverage, treated as image-based page"
    }