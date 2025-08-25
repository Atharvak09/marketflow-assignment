# MarketFlow Assignment

This project collects prediction market data from multiple sources, unifies the product names, and exports them to a CSV file.

---

## 1) Prerequisites
- Python 3.10+
- VS Code (recommended)

---

## 2) Setup
Clone the repository:
```bash
git clone https://github.com/Atharvak09/marketflow-assignment.git
cd marketflow-assignment

Create and activate a virtual environment:
# Windows
python -m venv .venv
.\.venv\Scripts\activate

# macOS/Linux
python3 -m venv .venv
source .venv/bin/activate

Install dependencies:
pip install -r requirements.txt

Run the Flow
python -m src.market_flow


Example Output
Console output:
✅ Collected Data: [
  {'site': 'polymarket.com', 'product': 'Trump wins 2024', 'price': 0.62},
  {'site': 'kalshi.com', 'product': 'Trump wins election 2024', 'price': 0.6},
  {'site': 'prediction-market.com', 'product': 'Biden wins 2024', 'price': 0.45},
  {'site': 'polymarket.com', 'product': 'Biden wins election 2024', 'price': 0.38}
]

✅ Unified Products: {
  'Trump wins 2024': [
    {'site': 'polymarket.com', 'price': 0.62},
    {'site': 'kalshi.com', 'price': 0.6}
  ],
  'Biden wins 2024': [
    {'site': 'prediction-market.com', 'price': 0.45},
    {'site': 'polymarket.com', 'price': 0.38}
  ]
}

CSV generated:
output_products.csv

Sample output_products.csv:
Product,Site,Price
Trump wins 2024,polymarket.com,0.62
Trump wins 2024,kalshi.com,0.60
Biden wins 2024,prediction-market.com,0.45
Biden wins 2024,polymarket.com,0.38
