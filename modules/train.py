from telegram import Update
from telegram.ext import ContextTypes

async def handle_train(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🏋️ Welcome to the training zone!\n"
        "Here you'll find fitness tips, nutrition advice, and mental toughness strategies.\n\n"
        "💪 /workout - Sample workouts\n"
        "🥗 /nutrition - Meal plans\n"
        "🧠 /mindset - Mindset training\n"
        "📈 More features coming soon!"
    )

