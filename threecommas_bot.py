import os
import requests
import time
from threecommas_api import ThreeCommas

# --- Configurable settings ---
PAIR = "BTC_GBP"
SPREAD = 5000                 # Grid covers ±£5,000 from center
GRID_LEVELS = 7               # Number of grid levels
ORDER_PERCENT = 0.10          # Fraction of GBP balance per grid order (10%)
REBALANCE_MARGIN = 0.25       # If price is >25% outside current grid, recenter

# --- Fetch live BTC/GBP price from Kraken ---
def fetch_live_kraken_price(pair="BTCGBP"):
    url = f"https://api.kraken.com/0/public/Ticker?pair={pair}"
    try:
        resp = requests.get(url, timeout=10).json()
        key = list(resp["result"].keys())[0]
        price = float(resp["result"][key]["c"][0])
        return price
    except Exception as e:
        print("Error fetching Kraken price:", e)
        return None

# --- Main gridbot automation logic ---
def main():
    # --- 1. Get API keys and init client ---
    API_KEY = os.getenv("THREECOMMAS_API_KEY")
    API_SECRET = os.getenv("THREECOMMAS_API_SECRET")
    if not API_KEY or not API_SECRET:
        raise Exception("Set your THREECOMMAS_API_KEY and THREECOMMAS_API_SECRET as environment variables!")
    tc = ThreeCommas(api_key=API_KEY, api_secret=API_SECRET)

    # --- 2. Find active GBP spot account ---
    accounts, error = tc.get_accounts()
    if error:
        raise Exception("Error fetching accounts:", error)
    ACCOUNT_ID = None
    for acc in accounts:
        if acc["currency_code"] == "GBP" and acc["active"]:
            ACCOUNT_ID = acc["id"]
            break
    if ACCOUNT_ID is None:
        raise Exception("No active GBP account found!")

    # --- 3. Get available GBP balance for order sizing ---
    balances, error = tc.get_account_table_balance(ACCOUNT_ID)
    if error:
        raise Exception("Error fetching balances:", error)
    available_gbp = None
    for bal in balances:
        if bal["currency"] == "GBP":
            available_gbp = float(bal["available"])
            break
    if available_gbp is None:
        raise Exception("No GBP balance found!")
    base_order_volume = round(available_gbp * ORDER_PERCENT, 2)
    if base_order_volume < 10:
        print("WARNING: Low balance may cause grid creation errors.")

    # --- 4. Fetch live BTC/GBP price from Kraken and compute new grid range ---
    live_price = fetch_live_kraken_price()
    if live_price is None:
        raise Exception("Couldn't fetch BTC/GBP price.")
    center_price = live_price
    min_price = round(center_price - SPREAD, 2)
    max_price = round(center_price + SPREAD, 2)

    print(f"\nLive BTC/GBP price: £{center_price}")
    print(f"Grid range: £{min_price} - £{max_price}, order size per level: £{base_order_volume}")

    # --- 5. Check for active bot and see if recentering is needed ---
    bots, error = tc.get_bots()
    if error:
        raise Exception("Error fetching bots:", error)
    active_bot = None
    for bot in bots:
        if bot["pair"] == PAIR and bot["is_enabled"]:
            active_bot = bot
            break

    need_recenter = False
    if active_bot:
        old_min = float(active_bot.get("min_price", 0))
        old_max = float(active_bot.get("max_price", 0))
        # If old bot is way off from the new price, flag for recentering
        if (center_price < old_min * (1 - REBALANCE_MARGIN) or
            center_price > old_max * (1 + REBALANCE_MARGIN)):
            need_recenter = True
        else:
            print("Grid bot already active and close to center. No recenter needed.")
    else:
        need_recenter = True

    # --- 6. Stop old bot if recentering is needed ---
    if active_bot and need_recenter:
        print(f"Stopping old grid bot '{active_bot['name']}' to recenter...")
        stop_result, stop_error = tc.disable_bot(active_bot['id'])
        if stop_error:
            print("Error stopping old bot:", stop_error)
        else:
            print("Old bot stopped.")

    # --- 7. Create a new grid bot if needed ---
    if need_recenter:
        print("Creating new grid bot centered at £{:.2f}...".format(center_price))
        bot_params = {
            "name": f"AutoGrid-{PAIR}-{int(time.time())}",
            "account_id": ACCOUNT_ID,
            "pair": PAIR,
            "base_order_volume": base_order_volume,
            "take_profit": 1.2,                 # % per grid
            "safety_order_volume": base_order_volume,
            "martingale_volume_coefficient": 1,
            "martingale_step_coefficient": 1,
            "max_safety_orders": 3,
            "active_safety_orders_count": 1,
            "safety_order_step_percentage": 1.5,
            "strategy_type": "long",
            "leverage_type": "not_specified",
            "grid_spacing": 0.5,                # % grid step
            "grid_levels": GRID_LEVELS,
            "min_price": min_price,
            "max_price": max_price,
            "stop_loss_percentage": 0,
            "take_profit_type": "total",
            "trailing_enabled": True
        }
        newbot, bot_error = tc.create_bot(bot_params)
        if bot_error:
            print("Error creating grid bot:", bot_error)
        else:
            print("New grid bot created:", newbot["name"])
    print("\nBot automation complete.\n")

if __name__ == "__main__":
    main()

