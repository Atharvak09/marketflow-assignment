import requests
from bs4 import BeautifulSoup
from crewai.flow.flow import Flow, listen, start
from crewai import Agent, Task
from litellm import completion
import csv

class MarketFlow(Flow):

    @start()
    def collect_data(self):
    
        data = [
            {"site": "polymarket.com", "product": "Trump wins 2024", "price": 0.62},
            {"site": "kalshi.com", "product": "Trump wins election 2024", "price": 0.60},
            {"site": "prediction-market.com", "product": "Biden wins 2024", "price": 0.45},
            {"site": "polymarket.com", "product": "Biden wins election 2024", "price": 0.38},
        ]
        print(" Collected Data:", data)
        return data


    @listen("collect_data")
    def unify_products(self, data):
        """Agent 2: Match same products across sites."""
       
        unified = {}
        for item in data:
            key = item["product"].lower().replace("election", "").strip()
            if key not in unified:
                unified[key] = []
            unified[key].append(item)

        print("\n Unified Products:", unified)
        return unified

    @listen("unify_products")
    def generate_csv(self, unified):
        """Agent 3: Save unified products into CSV."""
        filename = "output_products.csv"
        with open(filename, "w", newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Product", "Site", "Price"])
            for product, entries in unified.items():
                for e in entries:
                    writer.writerow([product, e["site"], e["price"]])

        print(f"\n CSV generated: {filename}")
        return filename


if __name__ == "__main__":
    flow = MarketFlow()
    flow.kickoff()
