from google import genai
import os

def run_vlm(image):
    try:
        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:
            raise ValueError("API key not found in environment")

        client = genai.Client(api_key=api_key)

        prompt = "Extract all readable text from this document page."

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=[prompt, image]
        )

        return response.text

    except Exception as e:
        print(f"⚠️ VLM failed: {e}")

        return {
            "error": "VLM_FAILED",
            "fallback": "OCR_USED"
        }