from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from kraken_client import get_price

import os
TELEGRAM_TOKEN = os.getenv("8175719917:AAF6OXKOGPj94qxjl9bYnuKuIz_s2PEKrdA")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello! I'm your trading bot. Type /trade to see BTC price.")

async def trade(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        price_data = get_price()
        price = price_data['result']['XXBTZUSD']['c'][0]
        await update.message.reply_text(f"Current BTC/USD price: ${price}")
    except Exception as e:
        await update.message.reply_text(f"Error: {e}")

app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("trade", trade))

app.run_polling()

