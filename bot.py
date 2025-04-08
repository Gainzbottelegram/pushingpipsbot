from dotenv import load_dotenv
import os

from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters
from kraken_client import get_price  # Make sure this is your custom function

# Load token from .env
load_dotenv()
TOKEN = os.getenv("TELEGRAM_TOKEN")

# --- Start Command ---
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

# --- Handlers ---
async def dashboard(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📊 Dashboard is in progress.\nHere you’ll track PnL, active trades & more!")

async def learn(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📚 Learn Mode:\nComing soon: bite-sized tips on trading, mindset & growth.\nStay tuned, champ! 💪"
    )

async def fitness_tips(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🔥 Fitness Tip:\n\"Discipline with your body reflects in your trading. Start your day with movement, even 10 pushups.\""
    )

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

# --- Bot Setup ---
app = ApplicationBuilder().token(TOKEN).build()

# Command + Button Handlers
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("trade", trade))
app.add_handler(MessageHandler(filters.Regex("📊 Dashboard"), dashboard))
app.add_handler(MessageHandler(filters.Regex("📚 Learn"), learn))
app.add_handler(MessageHandler(filters.Regex("🏋️‍♂️ Fitness Tips"), fitness_tips))
app.add_handler(MessageHandler(filters.Regex("💵 Trade Now"), trade))
app.add_handler(MessageHandler(filters.Regex("🧠 Daily Mindset Boost"), mindset_boost))
app.add_handler(MessageHandler(filters.Regex("⚙️ Settings"), settings))

# --- Run Bot ---
app.run_polling()
