# 🌐 Core Imports
import os
import sys
import logging
import asyncio

# 🧠 Third-party packages
import krakenex
import pandas as pd
from dotenv import load_dotenv

# 🤖 Telegram core
from telegram import Update, ReplyKeyboardMarkup, BotCommand, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
    CallbackQueryHandler,
)

# 🧩 GainzBot modules
from modules.main import handle_main
from modules.brain import handle_brain
from modules.train import handle_train
from modules.trade import handle_trade, connect_kraken
from modules.finance import check_balance, handle_finance, activate_trading_bot
from modules.fitness import handle_fitness
from modules.education import handle_education
from modules.mentor import handle_mentor

# Language & Tip Support
SUPPORTED_LANGUAGES = {
    "🇬🇧 English": "en",
    "🇪🇸 Español": "es",
    "🇫🇷 Français": "fr",
    "🇩🇪 Deutsch": "de"
}

translations = {
    "welcome": {
        "en": "Welcome to GainzBot 💪 Let's level up your body, bank, and brain.",
        "es": "Bienvenido a GainzBot 💪 Vamos a mejorar tu cuerpo, mente y billetera.",
        "fr": "Bienvenue sur GainzBot 💪 Élevons ton corps, ton portefeuille et ton esprit.",
        "de": "Willkommen bei GainzBot 💪 Lass uns Körper, Geld und Geist verbessern."
    },
    "choose_action": {
        "en": "Choose your next move:",
        "es": "Elige tu siguiente paso:",
        "fr": "Choisis ta prochaine étape :",
        "de": "Wähle deinen nächsten Schritt:"
    }
}

def get_user_lang(context, update):
    return context.user_data.get("lang") or update.effective_user.language_code[:2]

def t(key, lang):
    return translations.get(key, {}).get(lang, translations[key]["en"])

def get_tip(section, lang):
    sample = {
        "fitness": {
            "en": ["Train smart, not just hard."],
            "es": ["Entrena con inteligencia, no solo con fuerza."]
        },
        "finance": {
            "en": ["Risk small to gain big."],
            "es": ["Arriesga poco para ganar mucho."]
        }
    }
    tips = sample.get(section, {})
    return tips.get(lang, tips.get("en", ["Stay consistent."]))[0]

# Load environment variables
load_dotenv()
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
KRAKEN_API_KEY = os.getenv("KRAKEN_API_KEY")
KRAKEN_API_SECRET = os.getenv("KRAKEN_API_SECRET")

# Set up Kraken API
kraken = krakenex.API()

# Logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", 
    level=logging.INFO
)

# Initialize the application
app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

# Price fetcher (remove duplicates)
def get_price(pair="XXBTZUSD"):
    response = kraken.query_public("Ticker", {"pair": pair})
    price = response["result"][pair]["c"][0]
    return f"${price}"

# ✅ Define your slash menu commands
async def set_commands(bot):
    try:
        await bot.set_my_commands([
            BotCommand("start", "Launch GainzBot"),
            BotCommand("main", "📋 Main menu and bot settings"),
            BotCommand("train", "🏋️ Fitness & nutrition"),
            BotCommand("trade", "💸 Trading, finance, Kraken"),
            BotCommand("brain", "🧠 Mentorship & upgrades"),
        ])
        logging.info("Slash commands set")
    except Exception as e:
        logging.error(f"Failed to set commands: {e}")

# Define the /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    lang_code = user.language_code[:2]
    context.user_data["lang"] = lang_code

    welcome_text = (
        f"💪 Welcome to *GainzBot* — where your journey to *financial* and *physical* strength begins!\n\n"
        f"👋 Glad to have you onboard, {user.first_name}! Let’s get the gainz in!\n\n"
        f"🧠 Setting up your training zone...\n"
        f"✅ Account synced and active.\n"
        f"💵 Trading Style: Beginner-Friendly | 💭 Mindset Mode: On\n"
        f"⚙ ️ Status: Online | Latency: Optimal\n\n"
        f"🌍 Select your language:\n"
        f"🇺 🇸 English | 🇪🇸 Español (coming soon)\n\n"
        f"👇 Tap an option below to begin:"
    )
    keyboard = [
        ["📘 Learn", "💪 Fitness Tips"],
        ["💰 Trade Now", "⚙️ Settings"]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text(welcome_text, reply_markup=reply_markup, parse_mode="Markdown")

# ✅ Inline Language Selector Handler
async def language_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    keyboard = [
        [InlineKeyboardButton("🇺🇸 English", callback_data="lang_en")],
        [InlineKeyboardButton("⬅️ Back", callback_data="trade")]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await query.edit_message_text(
        "🌍 Choose your language:",
        reply_markup=reply_markup
    )

async def handle_language_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    lang = query.data.split("_")[1]
    context.user_data["lang"] = lang
    await query.edit_message_text(f"✅ Language set to: {lang.upper()}")

# --- Handlers ---
async def learn(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📚 Learn Mode:\nComing soon: bite-sized tips on trading, mindset & growth.\nStay tuned!💪")

async def fitness_tips(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        f"🔥 *Fitness Tip:*\nDiscipline with your body reflects in your trading. Start your day with movement, even 10 pushups.",
        parse_mode="Markdown"
    )

async def mindset_boost(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🧠 Boost:\n“Small steps every day beat huge leaps once in a while.”")

async def settings(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        ["💼 Risk Level", "💰 Trade Size"],
        ["🌙 Overnight Mode", "💸 Auto Withdrawals"],
        ["🌍 Change Language", "⬅️ Back to Main Menu"]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

    await update.message.reply_text(
        "⚙️ **Settings Panel:*\nCustomize your trading style below. Your account, your rules. 🧠💪\n\n"
        "👇 Choose an option to adjust:",
        parse_mode="Markdown",
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

async def back_to_main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        ["📘 Learn", "💪 Fitness Tips"],
        ["💰 Trade Now", "⚙️ Settings"]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text(
        "📋 Back to Main Menu:\nChoose an option below:",
        reply_markup=reply_markup
    )

# ✅ Background strategy runner
async def on_startup(app):
    print("✅ Breakout loop started")

# Add handlers
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("main", handle_main))
app.add_handler(CommandHandler("train", handle_train))
app.add_handler(CommandHandler("brain", handle_brain))
app.add_handler(CommandHandler("trade", handle_trade))
app.add_handler(CallbackQueryHandler(handle_main, pattern="main"))
app.add_handler(CallbackQueryHandler(handle_train, pattern="train"))
app.add_handler(CallbackQueryHandler(handle_brain, pattern="brain"))
app.add_handler(CallbackQueryHandler(handle_trade, pattern="trade"))
app.add_handler(CallbackQueryHandler(check_balance, pattern="^balance$"))
app.add_handler(CallbackQueryHandler(connect_kraken, pattern="^connect$"))
app.add_handler(MessageHandler(filters.Regex("📘 Learn"), learn))
app.add_handler(MessageHandler(filters.Regex("💪 Fitness Tips"), fitness_tips))
app.add_handler(MessageHandler(filters.Regex("💰 Trade Now"), handle_trade))
app.add_handler(MessageHandler(filters.Regex("⚙️ Settings"), settings))
app.add_handler(MessageHandler(filters.Regex("📈 Market Options"), market_options))
app.add_handler(MessageHandler(filters.Regex("🧯 Risk Level"), risk_level))
app.add_handler(MessageHandler(filters.Regex("📐 Trade Size"), trade_size))
app.add_handler(MessageHandler(filters.Regex("🌙 Overnight Trading"), overnight_trading))
app.add_handler(MessageHandler(filters.Regex("🔁 Auto Withdrawals"), auto_withdrawal))

# ✅ Full bot runner
def main():
    logging.info("Bot initializing")
    try:
        asyncio.run(set_commands(app.bot))
        logging.info("Slash commands set")
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        app.run_polling(allowed_updates=Update.ALL_TYPES)
        logging.info("Bot started")
        loop.run_forever()
    except Exception as e:
        logging.error(f"Bot failed to start: {e}")
    finally:
        app.stop()
        loop.close()

if __name__ == "__main__":
    main()