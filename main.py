from dotenv import load_dotenv
import os

load_dotenv()

gemini_key = os.getenv("GEMINI_API_KEY")
openrouter_key = os.getenv("OPENROUTER_API_KEY")
ocr_engine = os.getenv("OCR_ENGINE")
vlm_provider = os.getenv("VLM_PROVIDER")
output_dir = os.getenv("OUTPUT_DIR")

if not all([gemini_key, openrouter_key, ocr_engine, vlm_provider, output_dir]):
    raise ValueError("Missing required environment variables")

# 🔽 test block (temporary)
print("ENV LOADED SUCCESSFULLY")
print("OCR ENGINE:", ocr_engine)
print("VLM PROVIDER:", vlm_provider)
print("OUTPUT DIR:", output_dir)
print("GEMINI KEY LOADED:", bool(gemini_key))
print("OPENROUTER KEY LOADED:", bool(openrouter_key))