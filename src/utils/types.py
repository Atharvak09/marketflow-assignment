from dataclasses import dataclass
from typing import Optional, Dict

@dataclass
class Contract:
    source: str              # 'predictit' or 'manifold'
    market_id: str
    contract_id: str
    question: str
    outcome: str            # 'Yes' or 'No' or specific option
    yes_price: Optional[float]  # 0..1 probability/price for 'Yes'
    url: str
    extra: Dict
