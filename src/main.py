import os
import sys
import argparse
from dotenv import load_dotenv
from src.flow import build_flow, MODEL_ID

def main():
    here = os.path.abspath(__file__)
    root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    print(f"Running main.py from: {here}")
    print(f"Project working dir  : {root}")

    load_dotenv()

    gem_key = os.getenv("GEMINI_API_KEY")
    if not gem_key:
        print("\nERROR: GEMINI_API_KEY is not set. Create a .env file in the project root like:\n"
              "GEMINI_API_KEY=YOUR_REAL_KEY_HERE\n")
        sys.exit(1)
    print(f"GEMINI key loaded (tail): ...{gem_key[-4:]}  (hidden)")

    parser = argparse.ArgumentParser(description="Run CrewAI (Gemini) with keywords and threshold")
    parser.add_argument("--keywords", type=str, required=True, help="Comma separated keywords")
    parser.add_argument("--threshold", type=float, default=0.1, help="Relevance threshold (0–1)")
    args = parser.parse_args()

    crew = build_flow(args.keywords, args.threshold)

    print("\n🚀 Starting flow...\n")
    result = crew.kickoff()  
    print("\n✅ Crew finished! Output:\n")
    print(result)

if __name__ == "__main__":
    main()
