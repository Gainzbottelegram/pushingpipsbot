from dotenv import load_dotenv
import os

load_dotenv()  # Load variables from .env
TOKEN = os.getenv("TELEGRAM_TOKEN")

from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from kraken_client import get_price

from telegram import ReplyKeyboardMarkup
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    welcome_text = (
        f"💪 Welcome to GainzBot — where your journey to financial and physical strength begins!\n\n"
        f"👋 Glad to have you onboard, {user.first_name}!\n\n"
        f"📦 Setting up your training zone...\n"
        f"✅ Account synced and active.\n\n"
        f"📈 Trading Style: Beginner-Friendly | 🧠 Mindset Mode: On\n"
        f"⚙️ Status: Online | Latency: Optimal\n\n"
        f"🌍 Select your language:\n"
        f"🇺🇸 English | 🇪🇸 Español (coming soon)\n\n"
        f"👇 Tap an option below to begin:"
    )

    keyboard = [
        ["📊 Dashboard", "📚 Learn"],
        ["🏋️‍♂️ Fitness Tips", "💵 Trade Now"],
        ["🧠 Daily Mindset Boost", "⚙️ Settings"]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

    await update.message.reply_text(welcome_text, reply_markup=reply_markup)



async def trade(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        price_data = get_price()
        price = price_data['result']['XXBTZUSD']['c'][0]
        await update.message.reply_text(f"Current BTC/USD price: ${price}")
    except Exception as e:
        await update.message.reply_text(f"Error: {e}")

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("trade", trade))

app.run_polling()

