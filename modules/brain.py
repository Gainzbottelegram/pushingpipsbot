from telegram import Update
from telegram.ext import ContextTypes

async def handle_brain(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🧠 Welcome to GainzBot’s Mentorship Hub!\n\n"
        "This section is all about upgrading your MINDSET and skillset:\n"
        "📘 Learn – Dive into tutorials and strategy guides\n"
        "📊 Progress – Track your finance & fitness journey\n"
        "🚀 Upgrades – Unlock AI mentorship boosts\n"
        "🔗 Directory – Connect with the GainzBot elite\n\n"
        "Every choice you make here compounds. Let's grow smarter, stronger, wealthier."
    )

