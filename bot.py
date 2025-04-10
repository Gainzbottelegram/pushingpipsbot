import logging
import logging
import os
from telegram import ReplyKeyboardMarkup, Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)
from dotenv import load_dotenv
import krakenex
import pandas as pd

# Load environment variables
load_dotenv()
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
KRAKEN_API_KEY = os.getenv("KRAKEN_API_KEY")
KRAKEN_API_SECRET = os.getenv("KRAKEN_API_SECRET")

# Set up Kraken API
kraken = krakenex.API()
kraken.key = KRAKEN_API_KEY
kraken.secret = KRAKEN_API_SECRET

# Logging
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)

# Custom reply keyboard
keyboard = [
    ["📊 Dashboard", "🎓 Learn", "🏋️ Fitness Tips"],
    ["📈 Trade Now", "🧠 Daily Mindset Boost", "⚙️ Settings"]
]
reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

# Price fetch
def get_price(pair="XXBTZUSD"):
    response = kraken.query_public("Ticker", {"pair": pair})
    return f"${response['result'][pair]['c'][0]}"

# /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    welcome_message = (
        "Welcome to *GainzBot* – your personal coach for both *financial* and *physical* gains!💪\n\n"
        "📊 *Dashboard* – Real-time trading insights, daily motivation, and fitness guidance.\n"
        "📈 *Ready to level up?* Time to push some trades.\n"
        "👇 Choose an action below to begin 👇"
    )
    await update.message.reply_text(welcome_message, reply_markup=reply_markup, parse_mode="Markdown")

# Button/text responses
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_message = update.message.text

    if user_message == "📈 Trade Now":
        price = get_price()
        await update.message.reply_text(f"*Current BTC/USD:* {price}", parse_mode="Markdown")

    elif user_message == "🧠 Daily Mindset Boost":
        await update.message.reply_text("💬 *Discipline is choosing what you want most over what you want now.* Let’s get after it. 🔥", parse_mode="Markdown")

    elif user_message == "🏋️ Fitness Tips":
        await update.message.reply_text("🏃 *Quick tip:* Hustle. Drink water before you even feel thirsty. 💧")

    elif user_message == "🎓 Learn":
        await update.message.reply_text("📘 Free eBook dropping soon: *Trading 101 & Gym Hacks for Champions.*")

    elif user_message == "⚙️ Settings":
        await update.message.reply_text("⚙️ *Settings coming soon:* Market type, risk level, auto withdrawal & more!")

    elif user_message == "📊 Dashboard":
        await update.message.reply_text("📊 Your dashboard will soon show open trades, gainz, and goals. Stay tuned!")

    else:
        await update.message.reply_text("🤖 Not sure what that means, champ. Try hitting a button below.")

# Start the bot
if __name__ == "__main__":
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()
import os
from telegram import ReplyKeyboardMarkup, Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)
from dotenv import load_dotenv
import krakenex
import pandas as pd

# Load environment variables
load_dotenv()

# Get tokens from .env
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
KRAKEN_API_KEY = os.getenv("KRAKEN_API_KEY")
KRAKEN_API_SECRET = os.getenv("KRAKEN_API_SECRET")

# Set up Kraken API
kraken = krakenex.API()
kraken.key = KRAKEN_API_KEY
kraken.secret = KRAKEN_API_SECRET

# Set up logging
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)

# Custom reply keyboard
main_keyboard = [
    ["🏋️ Dashboard", "📚 Learn", "🔥 Fitness Tips"],
    ["📈 Trade Now", "🧠 Daily Mindset Boost", "⚙️ Settings"]
]
reply_markup = ReplyKeyboardMarkup(main_keyboard, resize_keyboard=True)

# Price fetcher
def get_price(pair="XXBTZUSD"):
    response = kraken.query_public("Ticker", {"pair": pair})
    price = response["result"][pair]["c"][0]
    return f"${price}"

# /start command handler
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    welcome_message = (
        "👋 Welcome to *GainzBot* – your personal coach for both *financial* and *physical* gains!\n\n"
        "Get pumped for real-time trading insights, daily motivation, and fitness guidance.\n\n"
        "💪 Ready to level up?\n\n"
        "Choose an option below to begin ⬇️"
    )
    await update.message.reply_text(welcome_message, reply_markup=reply_markup, parse_mode="Markdown")

# Message handler for menu buttons
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_message = update.message.text

    if user_message == "📈 Trade Now":
        price = get_price()
        await update.message.reply_text(f"🚀 BTC/USD is currently at *{price}*", parse_mode="Markdown")

    elif user_message == "🧠 Daily Mindset Boost":
        mindset_quote = "Discipline is choosing what you want most over what you want now. Let’s get after it. 💥"
        await update.message.reply_text(mindset_quote)

    elif user_message == "🔥 Fitness Tips":
        fitness_tip = "Hydration fuels your hustle. Drink water before you even feel thirsty. 🥤"
        await update.message.reply_text(fitness_tip)

    elif user_message == "📚 Learn":
        await update.message.reply_text("📘 Coming soon: Trading 101 & Gym Hacks for Champions.")

    elif user_message == "⚙️ Settings":
        await update.message.reply_text("⚙️ Settings coming soon: Market type, risk level, auto withdrawal & more!")

    elif user_message == "🏋️ Dashboard":
        await update.message.reply_text("📊 Your dashboard will soon show open trades, gains, and goals. Stay tuned!")

    else:
        await update.message.reply_text("Not sure what that means, champ. Try hitting a button below.")

# Run the bot
if __name__ == "__main__":
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("🤖 GainzBot is live and flexing!")
    app.run_polling()

