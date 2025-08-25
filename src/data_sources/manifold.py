import requests
from typing import List
from ..utils.types import Contract

MANIFOLD_ALL = "https://api.manifold.markets/v0/markets"

def fetch_manifold(limit: int = 500) -> List[Contract]:
    params = {"limit": limit}
    r = requests.get(MANIFOLD_ALL, params=params, timeout=45)
    r.raise_for_status()
    data = r.json()
    contracts: List[Contract] = []
    for m in data:
        if m.get("closeTime") and m.get("isResolved"):
            continue
        if m.get("outcomeType") != "BINARY":
            continue
        market_id = m.get("id")
        prob = m.get("probability")  # 0..1
        if prob is None:
            continue
        contracts.append(Contract(
            source="manifold",
            market_id=str(market_id),
            contract_id=str(market_id) + ":YES",
            question=m.get("question", ""),
            outcome="Yes",
            yes_price=float(prob),
            url=f"https://manifold.markets/{m.get('creatorUsername','')}/{m.get('slug','')}",
            extra={"volume": m.get("volume"), "liquidity": m.get("liquidity")}
        ))
    return contracts
