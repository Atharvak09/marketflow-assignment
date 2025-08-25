# CrowdWisdomTrading AI Agent — Starter (Beginner Friendly)

This repo is a **from-zero** starter for the assessment (CrewAI Poly task).
It is designed so you can first build a working rule‑based app, then (optionally)
wrap it with **CrewAI** agents.

---

## 0) Prereqs
- Python 3.10+
- VS Code (recommended)
- (Optional) OpenAI or Groq API key if you want to run the CrewAI version

---

## 1) Create & activate a virtual environment
```bash
# Windows (PowerShell)
python -m venv .venv
.\.venv\Scripts\activate

# macOS/Linux
python3 -m venv .venv
source .venv/bin/activate
```

## 2) Install dependencies
```bash
pip install -r requirements.txt
```

> If you want to use CrewAI with an LLM, set an API key (optional):
```bash
# OpenAI example
setx OPENAI_API_KEY "sk-..."
# or on macOS/Linux:
export OPENAI_API_KEY="sk-..."
```

## 3) Run the **working rule-based app** (no LLM needed)
The app fetches markets from **PredictIt** and **Manifold**, stores them in SQLite,
does fuzzy title matching, and finds simple opportunities where one site's "Yes" price
is **lower** than another site's implied probability by a threshold.

```bash
python src/main.py --keywords "election, trump, biden" --threshold 0.12
```

- Results are printed and also saved to `./out/opportunities.csv`.
- Data is stored in `./out/markets.db` (SQLite).

> Tip: Use broader or narrower keywords to control how many markets are compared.

## 4) (Optional) Run the **CrewAI** wrapper
This wraps the same logic into 3 agents:
- Scraper Agent → pulls data
- Analyst Agent → compares odds & finds edges
- Strategy Agent → proposes a simple bet plan

```bash
python src/run_crewai.py --keywords "election" --threshold 0.12
```

You’ll need an API key (e.g., `OPENAI_API_KEY` or `GROQ_API_KEY`) to run this.
If you don’t have one, **skip this step** — the rule-based app is enough to submit.

---

## 5) Project structure
```
src/
  main.py                  # rule-based CLI app (works without LLM)
  run_crewai.py            # optional CrewAI wrapper (needs API key)
  data_sources/
    predictit.py           # pulls public JSON from PredictIt
    manifold.py            # pulls public JSON from Manifold
  storage/
    db.py                  # SQLite with SQLAlchemy
  agents/
    crew_setup.py          # roles, tasks, crew wiring
    tools.py               # bridge tools used by CrewAI agents
  utils/
    matching.py            # fuzzy match helper
    types.py               # common dataclasses
requirements.txt
README.md
```

---

## 6) What to submit (suggested)
- A short demo video (screen recording) showing:
  1. `python src/main.py ...` runs and prints opportunities
  2. (Optional) `python src/run_crewai.py ...` producing a plan
- `opportunities.csv` produced by your run
- A short README note describing your approach

---

## 7) Notes & Ethics
- We use **public** JSON APIs for PredictIt and Manifold to avoid heavy scraping.
- Respect site terms and rate limits; this is **read-only** research.
- This starter focuses on **binary** markets for simplicity.

Good luck — you got this! 🚀
