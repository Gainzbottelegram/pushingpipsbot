import os
import krakenex
import asyncio
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder, CommandHandler, CallbackQueryHandler,
    MessageHandler, ContextTypes, filters
)

# --- Load environment variables ---
load_dotenv()
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
KRAKEN_API_KEY = os.getenv("KRAKEN_API_KEY")
KRAKEN_API_SECRET = os.getenv("KRAKEN_API_SECRET")

# --- Setup Kraken client ---
kraken = krakenex.API()
kraken.key = KRAKEN_API_KEY
kraken.secret = KRAKEN_API_SECRET

# --- Breakout Detection ---
async def check_breakout(pair="XBTUSD", interval="15", threshold=100):
    try:
        ohlc = kraken.query_public("OHLC", {"pair": pair, "interval": interval})
        if ohlc.get("error"):
            return f"Kraken Error: {ohlc['error']}"

        candles = ohlc["result"][list(ohlc["result"].keys())[0]]
        highs = [float(c[2]) for c in candles[-3:]]
        lows = [float(c[3]) for c in candles[-3:]]

        high_breakout = max(highs) - min(lows)
        if high_breakout >= threshold:
            return f"📈 Breakout detected on {pair}! Price moved ${high_breakout:.2f}"
        else:
            return f"No breakout yet. Movement: ${high_breakout:.2f}"
    except Exception as e:
        return f"⚠️ Error checking breakout: {str(e)}"

# --- Periodic detection task ---
async def breakout_loop(app):
    while True:
        msg = await check_breakout()
        print(msg)
        await asyncio.sleep(300)  # 5 minutes

# --- Command: /start ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        ["📊 Dashboard", "💵 Trade Now", "💡 Daily Mindset Boost"],
        ["🏋️ Fitness Tips", "⚙️ Settings"]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text(
        "🀟 Welcome to GainzBot!\n\n"
        "Your hybrid gym 🏋️ & trading coach is online.\n"
        "Let’s build both wealth and strength. Tap a button below to get started:",
        reply_markup=reply_markup
    )

# --- Trade Now handler ---
async def trade_now_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("💰 Deposit", callback_data="deposit_info")],
        [InlineKeyboardButton("🏧 Withdraw", callback_data="withdraw_info")],
        [InlineKeyboardButton("🔙 Back", callback_data="go_back")]
    ]
    reply_ markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "💰 Ready to move some funds?\n\nChose one of the options below to proceed:",
        reply_markup=reply_markup
    )

# --- Callback Handler for Deposit/Withdraw ---
async def trade_callbacks(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "deposit_info":
        await query.edit_message_text(
            text="Deposit steps coming soon. Log in to Kraken to begin."
        )
    elif query.data == "withdraw_info":
        await query.edit_message_text(
            text="Withdraw steps coming soon. Set up a wallet + secure address."
        )
    elif query.data == "go_back":
        await query.edit_message_text(
            text="📋 Choose your next step:",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("💰 Deposit", callback_data="deposit_info")],
                [InlineKeyboardButton("🏧 Withdraw", callback_data="withdraw_info")]
            ])
        )

# --- Fallback text handler ---

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if text == "💵 Trade Now":
        await trade_now_handler(update, context)
    else:
        await update.message.reply_text("🤖 Tap a button or use /start to begin.")

# --- Main ---
def main():
    global application
    application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    # Command + button handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(trade_callbacks))
    application.add_handler(MessageHandler(filters.Regex("💵 Trade Now"), trade_now_handler))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Background breakout checker (24/7 trading logic)
    application.create_task(breakout_loop(application))

    print("⚡️ GainzBot Kraken system is live!")
    application.run_polling()


if __name__ == "__main__":
    main()

