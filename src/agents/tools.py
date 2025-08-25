from typing import List, Dict
from ..data_sources.predictit import fetch_predictit
from ..data_sources.manifold import fetch_manifold
from ..utils.matching import is_potential_match
from ..utils.types import Contract

def gather_contracts(keywords: List[str]) -> List[Contract]:
    """Fetch and keyword‑filter contracts from multiple sources."""
    kws = [k.strip().lower() for k in keywords if k.strip()]
    allc = fetch_predictit() + fetch_manifold()
    if not kws:
        return allc
    return [c for c in allc if any(k in c.question.lower() for k in kws)]

def pairwise_matches(contracts: List[Contract]) -> List[Dict]:
    """Return pairs of potential cross‑site matches based on title similarity."""
    pairs = []
    pi = [c for c in contracts if c.source == "predictit"]
    mm = [c for c in contracts if c.source == "manifold"]
    for a in pi:
        for b in mm:
            if is_potential_match(a.question, b.question):
                pairs.append({
                    "predictit": a, "manifold": b
                })
    return pairs

def find_opportunities(pairs: List[Dict], threshold: float = 0.12) -> List[Dict]:
    """Simple edge: If Manifold prob - PredictIt price >= threshold → Buy on PredictIt
    or reverse. Returns a list with suggested action and expected edge."""
    ops = []
    for p in pairs:
        pa = p["predictit"]
        mb = p["manifold"]
        edge_m_minus_p = (mb.yes_price or 0) - (pa.yes_price or 0)
        edge_p_minus_m = (pa.yes_price or 0) - (mb.yes_price or 0)
        if edge_m_minus_p >= threshold:
            ops.append({
                "action": "BUY_YES_ON_PREDICTIT",
                "question": pa.question,
                "predictit_yes": pa.yes_price, "manifold_yes": mb.yes_price,
                "edge": round(edge_m_minus_p, 4),
                "links": {"predictit": pa.url, "manifold": mb.url}
            })
        elif edge_p_minus_m >= threshold:
            ops.append({
                "action": "BUY_YES_ON_MANIFOLD",
                "question": pa.question,  # same question
                "predictit_yes": pa.yes_price, "manifold_yes": mb.yes_price,
                "edge": round(edge_p_minus_m, 4),
                "links": {"predictit": pa.url, "manifold": mb.url}
            })
    # sort by biggest edge
    ops.sort(key=lambda x: x["edge"], reverse=True)
    return ops
