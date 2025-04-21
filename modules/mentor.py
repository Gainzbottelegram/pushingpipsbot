from telegram import Update
from telegram.ext import ContextTypes
import random

MINDSET_QUOTES = [
    "🧠 Discipline equals freedom. Stay consistent.",
    "💪 Small wins daily = huge gains weekly.",
    "⏳ Master patience — it’s your sharpest trading edge.",
    "🥶 Cold mind, hot market. Keep emotion out.",
    "📈 Growth mindset > market conditions."
]

async def handle_mentor(update: Update, context: ContextTypes.DEFAULT_TYPE):
    quote = random.choice(MINDSET_QUOTES)
    await update.message.reply_text(quote)


