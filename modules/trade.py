from telegram import Update
from telegram.ext import ContextTypes

async def handle_trade(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📈 Welcome to the GainzBot Trading Zone!\n\n"
        "Here’s where you manage your money and strategy:\n"
        "🔐 /connect — Link your Kraken account\n"
        "💵 /balance — Check funds\n"
        "⚡ /trade_now — Trigger auto-trading (breakouts)\n"
        "📊 /status — View live trading activity\n"
        "🧠 /strategy — Adjust trading logic & risk\n\n"
        "Let GainzBot earn while you train. You’ve got both in motion now. 💪💸"
    )

