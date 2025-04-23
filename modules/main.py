from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes

async def handle_main(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🏋️ Train", callback_data="train")],
        [InlineKeyboardButton("💸 Trade", callback_data="trade")],
        [InlineKeyboardButton("🧠 Brain", callback_data="brain")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "📋 Welcome to the GainzBot main menu!\n\n"
        "💪 Coach your body. 💰 Grow your money. 🧠 Train your mind.\n\n"
        "Choose your path below:",
        reply_markup=reply_markup
    )

