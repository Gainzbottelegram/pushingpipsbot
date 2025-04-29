# GainzBot Full Proper Rebuild

# =========================
# 📦 Core Imports
# =========================
import os
import asyncio
import logging
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, BotCommand
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler, ContextTypes, filters
)

# =========================
# 📂 Load Environment Variables
# =========================
load_dotenv()
TOKEN = os.getenv("TELEGRAM_TOKEN")

# =========================
# 🛠️ Setup Logging
# =========================
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", 
    level=logging.INFO
)

# =========================
# 💬 Price Fetcher Function
# =========================
from modules.finance import get_price  # Ensure this exists in modules/finance.py

# =========================
# 🌍 Inline Language Selector Handler
# =========================
async def language_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [
        [InlineKeyboardButton("🇬🇧 English", callback_data="lang_en"),
         InlineKeyboardButton("🇪🇸 Español", callback_data="lang_es")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("🌍 Please select your language:", reply_markup=reply_markup)

async def handle_language_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    if query.data == "lang_en":
        await query.edit_message_text("✅ Language set to English.")
    elif query.data == "lang_es":
        await query.edit_message_text("✅ Language set to Español.")

# =========================
# 🏠 Start / Main Menu
# =========================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    welcome_text = (
        f"💪 Welcome to *GainzBot* — Where Financial and Physical Strength Begin!\n\n"
        f"👋 Hi, {user.first_name}! Let's get those Gainz!\n\n"
        f"🌍 Language set: {context.user_data.get('lang', 'en').upper()}\n\n"
        f"👇 Choose a path to begin your journey:"
    )
    keyboard = [
        [InlineKeyboardButton("📋 Main", callback_data="main")],
        [InlineKeyboardButton("🏋️ Train", callback_data="train")],
        [InlineKeyboardButton("💸 Trade", callback_data="trade")],
        [InlineKeyboardButton("🧠 Brain", callback_data="brain")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(welcome_text, parse_mode="Markdown", reply_markup=reply_markup)

# =========================
# 📚 Button Callback Handlers
# =========================
async def handle_main(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.answer()
    await update.callback_query.edit_message_text("📋 Welcome to the Main Hub!")

async def handle_train(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.answer()
    await update.callback_query.edit_message_text("🏋️ Let's get your body right!")

async def handle_trade(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.answer()
    await update.callback_query.edit_message_text("💸 Syncing your trading setup...")

async def handle_brain(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.answer()
    await update.callback_query.edit_message_text("🧠 Boosting your Brain Gainz!")

# =========================
# 🔄 Strategy Breakout Runner (Placeholder)
# =========================
async def breakout_loop(app):
    while True:
        # Example: Fetch BTC Price
        btc_price = await asyncio.to_thread(get_price)
        print(f"[BREAKOUT SCAN] BTC Price: {btc_price}")
        await asyncio.sleep(60)

async def on_startup(app):
    app.create_task(breakout_loop(app))

# =========================
# 📋 Slash Menu Commands Setup
# =========================
async def set_commands(bot):
    await bot.set_my_commands([
        BotCommand("start", "🏠 Start your Gainz Journey"),
        BotCommand("main", "📋 Main Menu Options"),
        BotCommand("train", "🏋️ Training & Fitness"),
        BotCommand("trade", "💸 Trade Setup & Connect Kraken"),
        BotCommand("brain", "🧠 Mentorship & Upgrades"),
    ])

# =========================
# 🚀 Main Bot Runner
# =========================
async def main():
    app = ApplicationBuilder().token(TOKEN).post_init(on_startup).build()

    # Command Handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("main", handle_main))
    app.add_handler(CommandHandler("train", handle_train))
    app.add_handler(CommandHandler("trade", handle_trade))
    app.add_handler(CommandHandler("brain", handle_brain))

    # Inline Button Callback Handlers
    app.add_handler(CallbackQueryHandler(handle_main, pattern="^main$"))
    app.add_handler(CallbackQueryHandler(handle_train, pattern="^train$"))
    app.add_handler(CallbackQueryHandler(handle_trade, pattern="^trade$"))
    app.add_handler(CallbackQueryHandler(handle_brain, pattern="^brain$"))
    app.add_handler(CallbackQueryHandler(handle_language_callback, pattern="^lang_"))

    # Inline Language Selector Button
    app.add_handler(CommandHandler("language", language_handler))

    # Set Slash Commands
    await set_commands(app.bot)

    print("🤖 GainzBot is running and flexing!")
    await app.run_polling()

if __name__ == "__main__":
    asyncio.run(main())

