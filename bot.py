import logging
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import krakenex
import pandas as pd
from dotenv import load_dotenv

from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)
y
from telegram import ReplyKeyboardMarkup


from dotenv import load_dotenv
import krakenex
import pandas as pd


# Language & Tip Support
SUPPORTED_LANGUAGES = {
    "🇬🇧 English": "en",
    "🇪🇸 Español": "es",
    "🇷🇺 Русский": "ru",
    "🇫🇷 Français": "fr",
    "🇩🇪 Deutsch": "de"
}

translations = {
    "welcome": {
        "en": "Welcome to GainzBot 💪 Let's level up your body, bank, and brain.",
        "es": "Bienvenido a GainzBot 💪 Vamos a mejorar tu cuerpo, mente y billetera.",
        "ru": "Добро пожаловать в GainzBot 💪 Прокачаем тело, кошелёк и ум.",
        "fr": "Bienvenue sur GainzBot 💪 Élevons ton corps, ton portefeuille et ton esprit.",
        "de": "Willkommen bei GainzBot 💪 Lass uns Körper, Geld und Geist verbessern."
    },
    "choose_action": {
        "en": "Choose your next move:",
        "es": "Elige tu siguiente paso:",
        "ru": "Выберите следующее действие:",
        "fr": "Choisis ta prochaine étape :",
        "de": "Wähle deinen nächsten Schritt:"
    }
}

def get_user_lang(context, update):
    return context.user_data.get("lang") or update.effective_user.language_code[:2]

def t(key, lang):
    return translations.get(key, {}).get(lang, translations[key]["en"])

def get_tip(section, lang):
    # Placeholder – link to external tip loader in future
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
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)

# Custom reply keyboard
keyboard = [
    ["📊 Dashboard", "🎓 Learn", "🏋️ Fitness Tips"],
    ["💵 Trade Now", "🧠 Daily Mindset Boost", "⚙️ Settings"]
]
import krakenex
import pandas as pd
# Language & Tip Support
SUPPORTED_LANGUAGES = {
    "🇬🇧 English": "en",
    "🇪🇸 Español": "es",
    "🇷🇺 Русский": "ru",
    "🇫🇷 Français": "fr",
    "🇩🇪 Deutsch": "de"
}

translations = {
    "welcome": {
        "en": "Welcome to GainzBot 💪 Let's level up your body, bank, and brain.",
        "es": "Bienvenido a GainzBot 💪 Vamos a mejorar tu cuerpo, mente y billetera.",
        "ru": "Добро пожаловать в GainzBot 💪 Прокачаем тело, кошелёк и ум.",
        "fr": "Bienvenue sur GainzBot 💪 Élevons ton corps, ton portefeuille et ton esprit.",
        "de": "Willkommen bei GainzBot 💪 Lass uns Körper, Geld und Geist verbessern."
    },
    "choose_action": {
        "en": "Choose your next move:",
        "es": "Elige tu siguiente paso:",
        "ru": "Выберите следующее действие:",
        "fr": "Choisis ta prochaine étape :",
        "de": "Wähle deinen nächsten Schritt:"
    }
}

def get_user_lang(context, update):
    return context.user_data.get("lang") or update.effective_user.language_code[:2]

def t(key, lang):
    return translations.get(key, {}).get(lang, translations[key]["en"])

def get_tip(section, lang):
    # Placeholder – link to external tip loader in future
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

# Set up Kraken API

# Logging
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)

# Custom reply keyboard
keyboard = [
    ["📊 Dashboard", "🎓 Learn", "🏋️ Fitness Tips"],
    ["💵 Trade Now", "🧠 Daily Mindset Boost", "⚙️ Settings"],
    ["💼 Risk Level", "🎚 Trade Size"],
    ["🌙 Overnight Mode", "💸 Auto Withdrawals"]
]

reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

# Price fetch
def get_price(pair="XXBTZUSD"):
    response = kraken.query_public("Ticker", {"pair": pair})
    return f"${response['result'][pair]['c'][0]}"

# Language keyboard options
LANGUAGE_OPTIONS = [["🇺🇸 English", "🇪🇸 Español", "🇷🇺 Русский"]]
language_markup = ReplyKeyboardMarkup(LANGUAGE_OPTIONS, resize_keyboard=True, one_time_keyboard=True)

# Button/text responses
import importlib
finance = importlib.import_module("modules.finance")
handle_finance = finance.handle_finance
activate_trading_bot = finance.activate_trading_bot

from modules.fitness import handle_fitness
from modules.education import handle_education
from modules.mentor import handle_mentor

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if text == "📊 Dashboard":
        await update.message.reply_text("📈 Dashboard coming soon. You'll be able to view trade/flex stats here.")

    elif text == "🎓 Learn":
        await handle_education(update, context)

    elif text == "🏋️ Fitness Tips":
        await handle_fitness(update, context)

    elif text == "💰 Trade Now":
        await activate_trading_bot(update, context)

    elif text == "🧠 Daily Mindset Boost":
        await handle_mentor(update, context)

    elif text == "⚙️ Settings":
        await update.message.reply_text("⚙️ Settings menu coming soon: Change risk, language, and trading style.")

    elif text == "📉 Risk Level":
        await update.message.reply_text("🛡 Max risk per trade is currently set to 20% of your equity. Auto-sizing is enabled.")

    else:
        await update.message.reply_text("🤖 Not sure what that means, champ. Try hitting a button below.")

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
        ["📊 Dashboard", "🎓 Learn", "🏋️ Fitness Tips"],
        ["💵 Trade Now", "🧠 Daily Mindset Boost", "⚙️ Settings"],
        ["💼 Risk Level", "🎚 Trade Size"],
        ["🌙 Overnight Mode", "💸 Auto Withdrawals"],
        ["🌍 Change Language", "⬅️ Back"]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

    await update.message.reply_text(welcome_text, reply_markup=reply_markup, parse_mode="Markdown")

# Load environment variables
load_dotenv()
TOKEN = os.getenv("TELEGRAM_TOKEN")

# Set up logging
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)

# Run the bot
if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()


# Set up Kraken API

# Set up logging
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)

# Custom reply keyboard
async def back_to_main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        ["📊 Dashboard", "🎓 Learn", "🏋️ Fitness Tips"],
        ["💵 Trade Now", "🧠 Daily Mindset Boost", "⚙️ Settings"],
        ["💼 Risk Level", "🎚 Trade Size"],
        ["🌙 Overnight Mode", "💸 Auto Withdrawals"],
        ["🌍 Change Language", "⬅️ Back"]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

    await update.message.reply_text(
        "🏠 Back at base. Choose your next move👇",
        reply_markup=reply_markup
    )

# Price fetcher
def get_price(pair="XXBTZUSD"):
    response = kraken.query_public("Ticker", {"pair": pair})
    price = response["result"][pair]["c"][0]
    return f"${price}"


# Run the bot
if __name__ == "__main__":
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("🤖 GainzBot is live and flexing!")
    app.run_polling()

from kraken_client import get_price  # Make sure this is your custom function

# Load token from .env


# --- /start command ---
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
        ["📊 Dashboard", "🎓 Learn", "🏋️ Fitness Tips"],
        ["💵 Trade Now", "🧠 Daily Mindset Boost", "⚙️ Settings"],
        ["💼 Risk Level", "🎚 Trade Size"],
        ["🌙 Overnight Mode", "💸 Auto Withdrawals"],
        ["🌍 Change Language", "⬅️ Back"]
    ]

    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

    await update.message.reply_text(
        welcome_text,
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )
    
    # Send welcome message
    await update.message.reply_text(welcome_text, reply_markup=reply_markup, parse_mode="Markdown")


# --- Handlers ---
async def dashboard(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📊 Dashboard is in progress.\nHere you’ll track PnL, active trades & more!")

async def learn(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📚 Learn Mode:\nComing soon: bite-sized tips on trading, mindset & growth.\nStay tuned, champ! 💪")

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
        ["📊 Dashboard", "🎓 Learn", "🏋️ Fitness Tips"],
        ["💵 Trade Now", "🧠 Daily Mindset Boost", "⚙️ Settings"]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

    await update.message.reply_text(
        "⬅️ Back at base. No excuses. Choose your next move wisely. 💼🔥",
        reply_markup=reply_markup
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
app.add_handler(MessageHandler(filters.Regex("🔙 Back to Main Menu"), back_to_main_menu))
# --- Run Bot ---
app.run_polling()
async def language_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("🌍 Choose your preferred language:", reply_markup=language_markup)


# Start the bot
if __name__ == "__main__":
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
import krakenex
import pandas as pd

# Load environment variables

# Get tokens from .env

# Set up Kraken API

# Set up logging
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)


# Price fetcher
def get_price(pair="XXBTZUSD"):
    response = kraken.query_public("Ticker", {"pair": pair})
    price = response["result"][pair]["c"][0]
    return f"${price}"


# Run the bot
if __name__ == "__main__":
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("🤖 GainzBot is live and flexing!")
    app.run_polling()


from kraken_client import get_price  # Make sure this is your custom function

# Load token from .env

async def back_to_main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        ["📊 Dashboard", "🎓 Learn", "🏋️ Fitness Tips"],
        ["💵 Trade Now", "🧠 Daily Mindset Boost", "⚙️ Settings"]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

    await update.message.reply_text(
        "🏠 Back at base. Choose your next move👇",
        reply_markup=reply_markup
    )

# --- Bot Setup ---
if __name__ == "__main__":
    load_dotenv()
    TOKEN = os.getenv("TELEGRAM_TOKEN")

    app = ApplicationBuilder().token(TOKEN).build()

    # Add all handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("trade", trade))
    app.add_handler(MessageHandler(filters.Regex("📊 Dashboard"), dashboard))
    app.add_handler(MessageHandler(filters.Regex("🎓 Learn"), learn))
    app.add_handler(MessageHandler(filters.Regex("🏋 ️ Fitness Tips"), fitness_tips))
    app.add_handler(MessageHandler(filters.Regex("💵 Trade Now"), trade))
    app.add_handler(MessageHandler(filters.Regex("🧠 Daily Mindset Boost"), mindset_boost))
    app.add_handler(MessageHandler(filters.Regex("⚙ ️ Settings"), settings))
    app.add_handler(MessageHandler(filters.Regex("📉 Market Options"), market_options))
    app.add_handler(MessageHandler(filters.Regex("💼 Risk Level"), risk_level))
    app.add_handler(MessageHandler(filters.Regex("🎚 TTrade Size"), trade_size))
    app.add_handler(MessageHandler(filters.Regex("🌙 Overnight Trading"), overnight_trading))
    app.add_handler(MessageHandler(filters.Regex("💸 Auto Withdrawals"), auto_withdrawal))
    app.add_handler(MessageHandler(filters.Regex("⬅ ️ Back to Main Menu"), back_to_main_menu))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    app.run_polling()

