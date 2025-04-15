from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, ContextTypes, filters
from dotenv import load_dotenv
load_dotenv()
import os
import krakenex
from flask import Flask, request
import asyncio


# Initialize Flask app
app = Flask(__name__)

# Webhook URL (Replace with actual Railway URL)
WEBHOOK_URL = "https://railway.com/project/9bc0584c-9fb1-4287-8170-c6c991727782/service/bc396907-708e-44fb-b680-72e378fc7a24?environmentId=ad21b205-23ae-4f9b-a8ea-be41b72b6560"

# Load environment variables
load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
KRAKEN_API_KEY = os.getenv("KRAKEN_API_KEY")
KRAKEN_API_SECRET = os.getenv("KRAKEN_API_SECRET")

print(f"Token loaded: {TELEGRAM_TOKEN is not None}")

# Setup Kraken client
kraken = krakenex.API()
kraken.key = KRAKEN_API_KEY
kraken.secret = KRAKEN_API_SECRET


# Step 3: Set up the webhook route
@app.route("/YOUR_WEBHOOK_PATH", methods=["POST"])
async def webhook():
    json_str = request.get_data(as_text=True)
    update = Update.de_json(json_str, application.bot)
    
    # Process the update (e.g., call handlers here)
    application.process_update(update)
    
    return "OK", 200


# Deposit method: Generate Kraken deposit address (simplified example)
def get_deposit_address():
    try:
        res = kraken.query_private("DepositAddresses", {"asset": "XBT"})  # Replace 'XBT' with appropriate asset
        return res["result"]["XBT"]["address"]  # This returns the deposit address
    except Exception as e:
        print("Error fetching deposit address:", e)
        return "Error getting deposit address."


# Withdrawal method: Trigger a withdrawal (simplified example)
def trigger_withdrawal(amount, address):
    try:
        res = kraken.query_private("Withdraw", {"asset": "XBT", "key": "MyWithdrawalKey", "amount": amount, "address": address})
        return res
    except Exception as e:
        print("Error triggering withdrawal:", e)
        return "Error processing withdrawal."


# Fetch price
def get_price(pair="XXBTZUSD"):
    try:
        res = kraken.query_public("Ticker", {"pair": pair})
        return res["result"][pair]["c"][0]
    except Exception as e:
        print("Error fetching price:", e)
        return "N/A"


# Lessons for Learn module
lessons = [
    {
        "title": "Lesson 1: What Is Trading?",
        "content": "Trading means buying and selling assets to make a profit.\nCrypto = digital assets.\nForex = currencies like USD/JPY or EUR/GBP."
    },
    {
        "title": "Lesson 2: Forex vs Crypto",
        "content": "Forex: More stable, huge volume.\nCrypto: Volatile, 24/7.\nPick your arena, or trade both!"
    },
    {
        "title": "Lesson 3: Risk Management 101",
        "content": "✅ Always use a stop loss.\n❌ Don’t bet the farm.\n🎯 Control your risk, protect your capital!"
    },
    {
        "title": "Lesson 4: Mindset is the Muscle",
        "content": "Consistency > intensity.\nJust like the gym, small daily wins in trading compound over time.\nDiscipline = freedom."
    },
    {
        "title": "Lesson 5: Indicators & Price Action",
        "content": "Technical indicators like RSI, MACD, and EMAs help spot trends.\nBut price action is king — always read the chart."
    },
    {
        "title": "Lesson 6: Journaling Your Trades",
        "content": "Track every trade.\nWhat was the plan? What was the result?\nLike tracking reps and sets — reflection builds mastery."
    }
]


# Trade Now handler: Give user deposit/withdraw options
async def trade_now_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("💰 Deposit", callback_data="deposit_info")],
        [InlineKeyboardButton("🏧 Withdraw", callback_data="withdraw_info")],
        [InlineKeyboardButton("🔙 Back", callback_data="go_back")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "📥 Ready to move some funds?\n\nChoose one of the options below to proceed:",
        reply_markup=reply_markup
    )


# /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        ["📊 Dashboard", "💵 Trade Now", "💡 Daily Mindset Boost"],
        ["🏋️ Fitness Tips", "⚙️ Settings"]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text(
        "🏁 Welcome to GainzBot!\n\nYour hybrid gym 🏋️ & trading coach is online.\n\n"
        "Let’s build both wealth and strength. Tap a button below to get started:",
        reply_markup=reply_markup
    )


# Deposit handler function
async def deposit_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    deposit_address = get_deposit_address()  # Call the Kraken function to get the deposit address
    await update.message.reply_text(f"💰 To deposit Bitcoin (BTC), use this address:\n{deposit_address}\n\n"
                                    "Please ensure to only send BTC to this address.")


# Withdrawal handler function
async def withdrawal_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Here, we'll assume the user sends their amount and address as a message (e.g., '0.5 BTC 1A2B3C4D5E...')
    try:
        # Expect the message format: amount address (e.g., '0.5 BTC 1A2B3C4D5E...')
        text = update.message.text.split()
        amount = text[0]
        address = text[1]

        # Trigger withdrawal (ensure proper validation before doing this in production)
        result = trigger_withdrawal(amount, address)

        if isinstance(result, dict) and "result" in result:
            await update.message.reply_text(f"✅ Withdrawal of {amount} BTC initiated to {address}.")
        else:
            await update.message.reply_text(f"❌ Error processing withdrawal: {result}")
    except Exception as e:
        await update.message.reply_text(f"❌ Invalid input or error: {e}")


# Callback handler for deposit/withdraw actions
async def trade_callbacks(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "deposit_info":
        await query.edit_message_text(
            text=(
                "💰 *Deposit Info*\n\n"
                "1️⃣ Log in to your Kraken account.\n"
                "2️⃣ Go to Funding > Deposit.\n"
                "3️⃣ Choose your preferred coin (e.g., BTC or USDT).\n"
                "4️⃣ Copy the deposit address.\n"
                "5️⃣ Paste it into your wallet and send funds.\n\n"
                "[🔗 Kraken Deposit FAQ](https://support.kraken.com/hc/en-us/articles/360000675406)\n"
                "\n🔙 Use the button below to go back."
            ),
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back", callback_data="go_back")]])
        )

    elif query.data == "withdraw_info":
        await query.edit_message_text(
            text=(
                "🏧 *Withdraw Info*\n\n"
                "1️⃣ Log in to your Kraken account.\n"
                "2️⃣ Go to Funding > Withdraw.\n"
                "3️⃣ Select your asset (BTC, ETH, etc.).\n"
                "4️⃣ Add a withdrawal address.\n"
                "5️⃣ Confirm and withdraw securely.\n\n"
                "[🔗 Kraken Withdrawal FAQ](https://support.kraken.com/hc/en-us/articles/360000675323)\n"
                "\n🔙 Use the button below to go back."
            ),
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back", callback_data="go_back")]])
        )

    elif query.data == "go_back":
        await query.edit_message_text(
            text="📥 Choose an option below to continue:",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("💰 Deposit", callback_data="deposit_info")],
                [InlineKeyboardButton("🏧 Withdraw", callback_data="withdraw_info")]
            ])
        )


# Run bot
def main():
    global application
    application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(lesson_callback))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    application.add_handler(CallbackQueryHandler(trade_callbacks))

    print("⚡️ GainzBot is live!")
    application.run_polling()


if __name__ == "__main__":
    main()

