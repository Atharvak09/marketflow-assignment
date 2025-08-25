from crewai import Agent, Task, Crew, Process
from langchain.tools import tool
from typing import List
import os, json

from ..agents.tools import gather_contracts, pairwise_matches, find_opportunities

@tool
def fetch_markets_tool(keywords: str) -> str:
    """Fetch & filter markets for comma-separated keywords. Returns JSON list."""
    kws = [k.strip() for k in keywords.split(',') if k.strip()]
    contracts = gather_contracts(kws)
    return json.dumps([c.__dict__ for c in contracts], ensure_ascii=False)

@tool
def compare_markets_tool(contracts_json: str) -> str:
    """Compare markets across sites. Input: contracts JSON from fetch_markets_tool.
    Output: JSON list of potential matches."""
    import json
    from ..utils.types import Contract
    objs = json.loads(contracts_json)
    contracts = []
    for o in objs:
        contracts.append(Contract(**o))
    pairs = pairwise_matches(contracts)
    def normalize(p):
        return {
            "predictit": {**p["predictit"].__dict__},
            "manifold": {**p["manifold"].__dict__}
        }
    return json.dumps([normalize(p) for p in pairs], ensure_ascii=False)

@tool
def strategy_tool(pairs_json: str, threshold: float = 0.12) -> str:
    """Simple strategy: find opportunities with edge >= threshold. Returns JSON."""
    import json
    from ..utils.types import Contract
    pairs_raw = json.loads(pairs_json)
    # de-serialize
    pairs = []
    for p in pairs_raw:
        pa = Contract(**p["predictit"])
        mb = Contract(**p["manifold"])
        pairs.append({"predictit": pa, "manifold": mb})
    ops = find_opportunities(pairs, threshold=threshold)
    return json.dumps(ops, ensure_ascii=False, indent=2)

def build_crew():
    llm_model = os.getenv("OPENAI_MODEL","gpt-4o-mini")
    # Agents
    scraper = Agent(
        role="Market Scraper",
        goal="Collect up-to-date prediction market data for given topics.",
        backstory="You fetch public JSON from PredictIt & Manifold.",
        verbose=True,
        allow_delegation=False,
        tools=[fetch_markets_tool]
    )
    analyst = Agent(
        role="Odds Analyst",
        goal="Find cross-site matches and compute differences in implied probability.",
        backstory="You align similar questions and surface mismatches.",
        verbose=True,
        allow_delegation=False,
        tools=[compare_markets_tool]
    )
    strategist = Agent(
        role="Strategy Agent",
        goal="Produce a short list of opportunities with a simple action plan.",
        backstory="You apply a threshold rule to pick value bets.",
        verbose=True,
        allow_delegation=False,
        tools=[strategy_tool]
    )

    t1 = Task(
        description=(
            "Fetch markets for the provided keywords (comma-separated). Return raw JSON."
        ),
        agent=scraper,
        expected_output="JSON list of contracts"
    )
    t2 = Task(
        description=(
            "Take the JSON from Task 1, find cross-site matches of the same question. Return JSON pairs."
        ),
        agent=analyst,
        expected_output="JSON pairs of matched markets"
    )
    t3 = Task(
        description=(
            "Given pairs JSON and a threshold, compute opportunities and output a compact plan in JSON."
        ),
        agent=strategist,
        expected_output="JSON list of opportunities"
    )

    crew = Crew(agents=[scraper, analyst, strategist], tasks=[t1, t2, t3], process=Process.sequential)
    return crew
