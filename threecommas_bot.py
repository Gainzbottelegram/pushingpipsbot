import os
import requests

THREECOMMAS_API_KEY = os.environ['THREECOMMAS_API_KEY']
THREECOMMAS_API_SECRET = os.environ['THREECOMMAS_API_SECRET']
ACCOUNT_ID = 2038223 

API_URL = "https://api.3commas.io/public/api/ver1"

# Get 3c headers
def get_headers():
    return {
        'APIKEY': THREECOMMAS_API_KEY,
    }

# Check balance (update for your exchange)
def get_balance():
    url = f"{API_URL}/accounts/{ACCOUNT_ID}/load_balances"
    r = requests.get(url, headers=get_headers())
    return r.json()

# Create grid bot (fill in parameters as needed)
def create_grid_bot(pair="BTC_USDT", investment=10):
    url = f"{API_URL}/bots/create_grid_bot"
    payload = {
        "account_id": ACCOUNT_ID,
        "pair": pair,
        "base_order_volume": investment,
        "take_profit": 1.0,  # 1% TP
        # Add more grid parameters as needed
    }
    r = requests.post(url, headers=get_headers(), json=payload)
    return r.json()

if __name__ == "__main__":
    # Example: fetch balance, adjust investment based on size
    balances = get_balance()
    usdt_balance = float(balances.get('USDT', 0))
    investment = max(10, usdt_balance * 0.2)  # 20% of balance per bot

    # TODO: logic to pick the best pair (for now, hardcode)
    result = create_grid_bot(pair="BTC_USDT", investment=investment)
    print(result)

