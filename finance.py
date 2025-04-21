# modules/finance.py
import krakenex
from telegram import Update
from telegram.ext import ContextTypes
import os
from dotenv import load_dotenv

load_dotenv()
api = krakenex.API()
api.load_key('kraken.key')  # Or use os.getenv("KRAKEN_KEY") & ("KRAKEN_SECRET")

async def handle_finance(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📊 Finance mode activated. Type /price to check BTC/USD or tap '⚡ Activate Trading' to begin.")

async def activate_trading_bot(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # SAFETY: Just print prices for now. No live trades.
    pair = "XXBTZUSD"
    try:
        response = api.query_public('Ticker', {'pair': pair})
        price = response['result'][pair]['c'][0]
        await update.message.reply_text(f"💡 Breakout scanner is watching BTC/USD.\nCurrent price: ${price}\n\nNo trades will be placed until live mode is confirmed.")
    except Exception as e:
        await update.message.reply_text(f"⚠️ Error accessing Kraken: {str(e)}")

