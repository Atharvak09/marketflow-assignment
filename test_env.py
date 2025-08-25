import os
from dotenv import load_dotenv

load_dotenv()

print("Gemini key is:", os.getenv("GEMINI_API_KEY"))
