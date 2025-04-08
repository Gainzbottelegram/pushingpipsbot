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
async def dashboard(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📊 Dashboard is warming up — you’ll soon see all your performance metrics!")

async def learn(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📚 Learn Hub launching soon — trading lessons, mindset hacks, and more.")

async def fitness_tips(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🔥 Fitness Tip:\n“Start your day with movement — 20 push-ups clears the fog.”")

async def trade(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        price_data = get_price()
        price = price_data['result']['XXBTZUSD']['c'][0]
        await update.message.reply_text(f"💸 Current BTC/USD price: ${price}")
    except Exception as e:
        await update.message.reply_text(f"⚠️ Error fetching price: {e}")

async def mindset_boost(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🧠 Boost:\n“Small steps every day beat huge leaps once in a while.”")

async def settings(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("⚙️ Settings coming soon! You'll control risk, alerts & more.")



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
app.add_handler(MessageHandler(filters.Regex("📊 Dashboard"), dashboard))
app.add_handler(MessageHandler(filters.Regex("📚 Learn"), learn))
app.add_handler(MessageHandler(filters.Regex("🔥 Fitness Tips"), fitness_tips))
app.add_handler(MessageHandler(filters.Regex("💸 Trade Now"), trade))
app.add_handler(MessageHandler(filters.Regex("🧠 Daily Mindset Boost"), mindset_boost))
app.add_handler(MessageHandler(filters.Regex("⚙️ Settings"), settings))


app.run_polling()

