from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, ContextTypes, filters
from dotenv import load_dotenv
import os
import krakenex
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

# Load environment variables
load_dotenv()
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
KRAKEN_API_KEY = os.getenv("KRAKEN_API_KEY")
KRAKEN_API_SECRET = os.getenv("KRAKEN_API_SECRET")

# Setup Kraken client
kraken = krakenex.API()
kraken.key = KRAKEN_API_KEY
kraken.secret = KRAKEN_API_SECRET

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

# Reply keyboard message handler
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower()
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

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower()

    if "trade" in text:
        await trade_now_handler(update, context)
    elif "deposit" in text:
        await deposit_handler(update, context)
    elif "withdraw" in text:
        await withdrawal_handler(update, context)
    elif "dashboard" in text:
        await update.message.reply_text("📊 Dashboard coming soon! All your gains in one view.")
    elif "learn" in text:
        await start_learning(update, context)
    elif "daily mindset" in text:
        await update.message.reply_text("💪 Trading & lifting tips coming your way.")
    elif "fitness" in text:
        await update.message.reply_text("🏋️‍♂️ **Strong mind. Strong trades. Strong body.**")
    elif "settings" in text:
        await update.message.reply_text("⚙️ Settings page coming soon. Customize your strategy.")
    else:
        await update.message.reply_text("🤔 Not sure what you mean. Try the buttons above!")

# /learn command
async def learn(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton("📘 Start Learning", callback_data="lesson_0")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "📘 Ready to boost your trading brain?\nTap below to begin the first lesson!",
        reply_markup=reply_markup
    )

# Callback handler for lesson navigation
async def lesson_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    lesson_index = int(query.data.split("_")[1])
    lesson = lessons[lesson_index]

    text = f"🧠 *{lesson['title']}*\n\n{lesson['content']}"
    buttons = []

    if lesson_index > 0:
        buttons.append(InlineKeyboardButton("⬅️ Back", callback_data=f"lesson_{lesson_index - 1}"))
    if lesson_index < len(lessons) - 1:
        buttons.append(InlineKeyboardButton("➡️ Next", callback_data=f"lesson_{lesson_index + 1}"))

    reply_markup = InlineKeyboardMarkup([buttons]) if buttons else None
    await query.edit_message_text(text=text, reply_markup=reply_markup, parse_mode="Markdown")

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
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("learn", learn))
    app.add_handler(CallbackQueryHandler(lesson_callback))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_handler(CallbackQueryHandler(trade_callbacks))

    print("⚡️ GainzBot is live!")
    app.run_polling()

if __name__ == "__main__":
    main()

