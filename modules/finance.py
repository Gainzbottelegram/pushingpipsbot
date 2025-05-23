import krakenex
import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ContextTypes

load_dotenv()

api = krakenex.API(
    os.getenv("KRAKEN_API_KEY"),
    os.getenv("KRAKEN_API_SECRET")
)

breakout_running = False
high_trigger = 72000.0
low_trigger = 69000.0
pair = "XXBTZUSD"
asset = "XXBT"

# ✅ Main handler for when user presses "📈 Finance"
async def handle_finance(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📊 Finance activated.\nUse 💰 Trade Now to begin breakout scanning and auto trading.")

# ✅ Triggers background breakout monitoring and auto-trading
async def activate_trading_bot(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global breakout_running
    if breakout_running:
        await update.message.reply_text("⚠️ Already monitoring BTC/USD for breakout.")
        return

    breakout_running = True
    await update.message.reply_text("📡 GainzBot is now watching BTC/USD...\nLive trades will auto-execute using 20% of balance.")

async def monitor_breakout():
    global breakout_running
    breakout_running = True

    try:
        balance_data = api.query_private('Balance')
        print(f"[GAINZBOT DEBUG] Raw Balance Response: {balance_data}")

        preferred_currencies = ["ZUSD", "ZGBP", "USDT", "ZEUR"]
        usd_balance = 0.0
        currency_used = None

        for currency in preferred_currencies:
            if currency in balance_data["result"]:
                usd_balance = float(balance_data["result"][currency])
                currency_used = currency
                break

        print(f"[GAINZBOT DEBUG] Balance Detected: {usd_balance} in {currency_used}")

        if usd_balance == 0:
            await update.message.reply_text(
                "❌ No balance available in USD, GBP, USDT, or EUR. Add funds to begin trading."
            )
            breakout_running = False
            return

        risk_equity = usd_balance * 0.20

        import asyncio
        while breakout_running:
            response = api.query_public('Ticker', {'pair': pair})
            if 'result' not in response or pair not in response['result']:
                await update.message.reply_text("⚠️ No price available. Kraken API returned an unexpected response.")
                breakout_running = False
                return

            price = float(response['result'][pair]['c'][0])
            print(f"[GAINZBOT DEBUG] Price response: {price}")

            if price > high_trigger:
                await update.message.reply_text(f"🚀 Breakout UP! BTC/USD hit ${price}")
                await place_trade(update, price, "buy", risk_equity)
                breakout_running = False

            elif price < low_trigger:
                await update.message.reply_text(f"📉 Breakout DOWN! BTC/USD dropped to ${price}")
                await place_trade(update, price, "sell", risk_equity)
                breakout_running = False

            await asyncio.sleep(10)

    except Exception as e:
        breakout_running = False
        await update.message.reply_text(f"⚠️ Error: {str(e)}")

    import asyncio
    asyncio.create_task(monitor_breakout())

# ✅ Executes a live market order with SL & TP
async def place_trade(update: Update, price: float, direction: str, risk_amount: float):
    try:
        volume = round(risk_amount / price, 6)

        if direction == "buy":
            stop_price = round(price * 0.985, 2)
            profit_price = round(price * 1.025, 2)
        else:
            stop_price = round(price * 1.015, 2)
            profit_price = round(price * 0.975, 2)

        order = api.query_private('AddOrder', {
            'pair': pair,
            'type': direction,
            'ordertype': 'market',
            'volume': volume,
            'close[ordertype]': 'take-profit',
            'close[price]': profit_price,
            'leverage': 'none',
            'stopprice': stop_price
        })

        if order['error']:
            await update.message.reply_text(f"❌ Trade failed: {order['error']}")
        else:
            txid = order['result']['txid'][0]
            await update.message.reply_text(
                f"✅ Trade executed: {direction.upper()} {volume} BTC at ${price}\n"
                f"🎯 TP: ${profit_price} | 🛑 SL: ${stop_price}\n"
                f"🔁 TXID: {txid}"
            )
    except Exception as e:
        await update.message.reply_text(f"⚠️ Trade error: {str(e)}")

async def check_balance(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        balance_data = api.query_private('Balance')
        preferred_currencies = ["ZUSD", "ZGBP", "USDT", "ZEUR"]
        fiat_balance = 0.0
        currency_used = None

        for currency in preferred_currencies:
            if currency in balance_data["result"]:
                fiat_balance = float(balance_data["result"][currency])
                currency_used = currency
                break

        btc_balance = balance_data["result"].get("XXBT", "0")

        await update.message.reply_text(
            f"💼 Your Kraken Balance:\n\n"
            f"{currency_used}: {fiat_balance}\n"
            f"₿ BTC: {btc_balance}"
        )

    except Exception as e:
        await update.message.reply_text(f"⚠️ Could not fetch balance: {str(e)}")

