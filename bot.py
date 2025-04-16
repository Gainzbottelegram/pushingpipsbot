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


# Language & Tip Support
SUPPORTED_LANGUAGES = {
    "🇺🇸 English": "en",
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
kraken.key = KRAKEN_API_KEY
kraken.secret = KRAKEN_API_SECRET

# Logging
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)

# Custom reply keyboard
keyboard = [
    ["📊 Dashboard", "🎓 Learn", "🏋️ Fitness Tips"],
    ["📈 Trade Now", "🧠 Daily Mindset Boost", "⚙️ Setting"]
]

settings_keyboard = [
    ["💼 Risk Level", "🎚 Trade Size"],
    ["🌙 Overnight Mode", "💸 Auto Withdrawals"],
    ["🌍 Change Language", "⬅️ Back"]
],
    ["📈 Trade Now", "🧠 Daily Mindset Boost", "⚙️ Settings", "🌍 Language"]
]
reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

# Price fetch
def get_price(pair="XXBTZUSD"):
    response = kraken.query_public("Ticker", {"pair": pair})
    return f"${response['result'][pair]['c'][0]}"

# Language keyboard options
LANGUAGE_OPTIONS = [["🇺🇸 English", "🇪🇸 Español", "🇷🇺 Русский"]]
language_markup = ReplyKeyboardMarkup(LANGUAGE_OPTIONS, resize_keyboard=True, one_time_keyboard=True)

# Handle "🌍 Language" button tap
async def language_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("🌍 Choose your preferred language:", reply_markup=language_markup)

# /start command

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang_code = update.effective_user.language_code[:2]
    context.user_data["lang"] = lang_code

    welcome_msg = t("welcome", lang_code)
    choose_msg = t("choose_action", lang_code)

    await update.message.reply_text(welcome_msg)
    await update.message.reply_text(choose_msg, reply_markup=reply_markup)
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

    elif user_message == "🌍 Language":
        await language_handler(update, context)

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
    ["📊 Dashboard", "🎓 Learn", "🏋️ Fitness Tips"],
    ["📈 Trade Now", "🧠 Daily Mindset Boost", "⚙️ Settings"]
]

settings_keyboard = [
    ["💼 Risk Level", "🎚 Trade Size"],
    ["🌙 Overnight Mode", "💸 Auto Withdrawals"],
    ["🌍 Change Language", "⬅️ Back"]
],
    ["📈 Trade Now", "🧠 Daily Mindset Boost", "⚙️ Settings"]
]
reply_markup = ReplyKeyboardMarkup(main_keyboard, resize_keyboard=True)

# Price fetcher
def get_price(pair="XXBTZUSD"):
    response = kraken.query_public("Ticker", {"pair": pair})
    price = response["result"][pair]["c"][0]
    return f"${price}"

# /start command handler

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang_code = update.effective_user.language_code[:2]
    context.user_data["lang"] = lang_code

    welcome_msg = t("welcome", lang_code)
    choose_msg = t("choose_action", lang_code)

    await update.message.reply_text(welcome_msg)
    await update.message.reply_text(choose_msg, reply_markup=reply_markup)
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
    print("🤖 GainzBot is live and shining!")
    app.run_polling()

=======
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
    lang_code = update.effective_user.language_code[:2]
    context.user_data["lang"] = lang_code

    welcome_msg = t("welcome", lang_code)
    choose_msg = t("choose_action", lang_code)

    await update.message.reply_text(welcome_msg)
    await update.message.reply_text(choose_msg, reply_markup=reply_markup)
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
    ["📊 Dashboard", "🎓 Learn", "🏋️ Fitness Tips"],
    ["📈 Trade Now", "🧠 Daily Mindset Boost", "⚙️ Settings"]
]

settings_keyboard = [
    ["💼 Risk Level", "🎚 Trade Size"],
    ["🌙 Overnight Mode", "💸 Auto Withdrawals"],
    ["🌍 Change Language", "⬅️ Back"]
],
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
    ["📊 Dashboard", "🎓 Learn", "🏋️ Fitness Tips"],
    ["📈 Trade Now", "🧠 Daily Mindset Boost", "⚙️ Settings"]
]

settings_keyboard = [
    ["💼 Risk Level", "🎚 Trade Size"],
    ["🌙 Overnight Mode", "💸 Auto Withdrawals"],
    ["🌍 Change Language", "⬅️ Back"]
],
        ["💰 Trade Size", "🌙 Overnight Trading"],
        ["🏦 Auto Withdrawal", "🔙 Back to Main Menu"]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

    await update.message.reply_text(
        "⚙️ Settings Panel:\nCustomize your trading style below. Your account, your rules. 💼\n\n"
        "Choose an option:",
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
    ["📈 Trade Now", "🧠 Daily Mindset Boost", "⚙️ Settings"]
]

settings_keyboard = [
    ["💼 Risk Level", "🎚 Trade Size"],
    ["🌙 Overnight Mode", "💸 Auto Withdrawals"],
    ["🌍 Change Language", "⬅️ Back"]
],
        ["🏋️‍♂️ Fitness Tips", "💵 Trade Now"],
        ["🧠 Daily Mindset Boost", "⚙️ Settings"]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

    await update.message.reply_text(
        "🏠 Back at base. Choose your next move👇",
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

