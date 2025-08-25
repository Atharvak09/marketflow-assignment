import requests
from typing import List
from ..utils.types import Contract

PREDICTIT_ALL = "https://api.predictit.org/api/marketdata/all"


def fetch_predictit() -> List[Contract]:
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/115.0 Safari/537.36"
    }
    r = requests.get(PREDICTIT_ALL, headers=headers, timeout=30)
    r.raise_for_status()
    data = r.json()
    contracts: List[Contract] = []
    for m in data.get("markets", []):
        market_id = str(m.get("id"))
        question = m.get("name", "")
        url = m.get("url", "")
        for c in m.get("contracts", []):
            cid = str(c.get("id"))
            # prefer bestBuyYesCost; fallback to lastTradePrice
            yes = c.get("bestBuyYesCost")
            if yes is None:
                yes = c.get("lastTradePrice")
            if yes is None:
                continue
            # Normalize: prices are in 0..1 already
            contracts.append(Contract(
                source="predictit",
                market_id=market_id,
                contract_id=cid,
                question=question,
                outcome=c.get("name", "Yes"),
                yes_price=float(yes),
                url=url,
                extra={"image": m.get("image"), "status": m.get("status")}
            ))
    return contracts
