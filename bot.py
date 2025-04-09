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
    keyboard = [
        ["🌍 Market Options", "⚠️ Risk Level"],
        ["💰 Trade Size", "🌙 Overnight Trading"],
        ["🔄 Auto Withdrawal"]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

    await update.message.reply_text(
        "⚙️ Settings Hub:\nPersonalize your GainzBot experience.\n\n"
        "You’re in control — like any pro trader or athlete. 💼💪",
        reply_markup=reply_markup
    )

async def market_options(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🌍 Market Options:\nChoose what you want to trade.\n\n"
        "🔹 Crypto (BTC, ETH, etc.)\n"
        "🔹 Forex (EUR/USD, GBP/JPY, etc.)\n\n"
        "Your bot is 24/7 ready — just select your arena."
    )

async def risk_level(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "⚠️ Risk Level:\nSet your preferred trading risk.\n\n"
        "🟢 Low (Steady gains)\n🟡 Medium (Balanced approach)\n🔴 High (Aggressive strategies)\n\n"
        "Coach’s tip: Consistency beats chaos."
    )

async def trade_size(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "💰 Trade Size:\nDefine how much to risk per trade.\n\n"
        "Examples:\n- $10 per trade\n- 5% of your balance\n\n"
        "💡 Smart sizing protects your gains!"
    )

async def overnight_trading(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🌙 Overnight Trading:\nShould GainzBot stay active while you sleep?\n\n"
        "✅ Yes — I want round-the-clock trades\n❌ No — Pause during rest hours\n\n"
        "💤 Recovery is growth — in life and in markets."
    )

async def auto_withdrawal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🔄 Auto Withdrawal:\nSet up automatic profit pulls.\n\n"
        "💸 Options:\n- Weekly\n- Monthly\n- After 10% gain\n\n"
        "💼 Secure the bag, consistently."
    )

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
app.add_handler(MessageHandler(filters.Regex("🌍 Market Options"), market_options))
app.add_handler(MessageHandler(filters.Regex("⚠️ Risk Level"), risk_level))
app.add_handler(MessageHandler(filters.Regex("💰 Trade Size"), trade_size))
app.add_handler(MessageHandler(filters.Regex("🌙 Overnight Trading"), overnight_trading))
app.add_handler(MessageHandler(filters.Regex("🔄 Auto Withdrawal"), auto_withdrawal))

# --- Run Bot ---
app.run_polling()
