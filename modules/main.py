from telegram import Update
from telegram.ext import ContextTypes

async def handle_main(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🏠 Welcome to the GainzBot main menu!\n\n"
        "💪 Coach your body. 💰 Grow your money. 🧠 Train your mind.\n\n"
        "Try one of these:\n"
        "/train – Fitness, Nutrition, Mindset\n"
        "/trade – Trading, Finance, Setup\n"
        "/brain – Mentorship, Education, Upgrades"
    )

