import argparse, json, os
from .agents.crew_setup import build_crew

def main():
    parser = argparse.ArgumentParser(description="CrewAI wrapper for odds comparison")
    parser.add_argument("--keywords", type=str, default="election", help="Comma-separated keywords")
    parser.add_argument("--threshold", type=float, default=0.12)
    args = parser.parse_args()

    crew = build_crew()
    # Orchestrate: we pass 'inputs' that agents can reference in LLM prompts
    result = crew.kickoff(inputs={
        "keywords": args.keywords,
        "threshold": args.threshold
    })
    # Depending on CrewAI version, result may be a string; print as-is
    print("\n=== CrewAI Output ===\n")
    print(result)

if __name__ == "__main__":
    main()
