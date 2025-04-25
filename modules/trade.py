from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes

async def handle_trade(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("📈 Market Options", callback_data="market_options")],
        [InlineKeyboardButton("💼 Risk Level", callback_data="risk_level")],
        [InlineKeyboardButton("💰 Trade Size", callback_data="trade_size")],
        [InlineKeyboardButton("🌙 Overnight Trading", callback_data="overnight_trading")],
        [InlineKeyboardButton("🔁 Auto Withdrawals", callback_data="auto_withdrawal")],
        [InlineKeyboardButton("💳 Check Balance", callback_data="balance")],
        [InlineKeyboardButton("🔗 Connect Kraken", callback_data="connect")],
        [InlineKeyboardButton("⬅️ Back", callback_data="main_menu")],
    ]

async def connect_kraken(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(
        text="🔗 Connect your Kraken account:\nComing soon. We’ll walk you through API key setup and account sync."
    )


    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("⚙️ Customize your trading settings:", reply_markup=reply_markup)

