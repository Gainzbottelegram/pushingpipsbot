from telegram import Update
from telegram.ext import ContextTypes

async def handle_education(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📘 Learn module coming soon — you'll get educational tips, trading breakdowns, and more!")

