import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# Configuration
BOT_TOKEN = "8878827364:AAHk-sX2zvipBvkwukaW83Y-ht-S-2e8tbg"
ADMIN_USERNAME = "@PKRT_Pay_Bot"
PRIVACY_URL = "https://telegra.ph/PKRT-Official-Ecosystem---Privacy-Policy-08-31"

# CPA Offers Links
CPA_OFFER_1 = "https://singingfiles.com/show.php?l=0&u=2553910&id=75155&tracking_id=PKRT"
CPA_OFFER_2 = "https://singingfiles.com/show.php?l=0&u=2553910&id=74385&tracking_id=PKRT"
CPA_OFFER_3 = "https://singingfiles.com/show.php?l=0&u=2553910&id=74388&tracking_id=PKRT"
CPA_OFFER_4 = "https://singingfiles.com/show.php?l=0&u=2553910&id=59478&tracking_id=PKRT"
CPA_OFFER_5 = "https://singingfiles.com/show.php?l=0&u=2553910&id=59479&tracking_id=PKRT"
CPA_OFFER_6 = "https://singingfiles.com/show.php?l=0&u=2553910&id=74386&tracking_id=PKRT"

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

user_balances = {}

def get_balance(user_id):
    return user_balances.get(user_id, 0.0)

def add_balance(user_id, amount):
    user_balances[user_id] = round(get_balance(user_id) + amount, 2)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    user_id = user.id
    
    if user_id not in user_balances:
        user_balances[user_id] = 0.0

    welcome_text = (
        f"🇵🇰 **Welcome to PKRT Official Ecosystem!** 🇵🇰\n\n"
        f"Hello {user.first_name}! Complete CPA offers and tasks to earn PKRT stablecoin rewards.\n\n"
        f"📊 **Base Value:** 1 PKRT = 1 PKR\n"
        f"💸 **Minimum Cashout:** 1.00 PKRT\n\n"
        f"🌟 **Features:**\n"
        f"• 🎁 Daily Check-in Rewards\n"
        f"• 📋 CPA Tasks & Surveys\n"
        f"• 🔒 5-Year Vault (Target: 1 USDT)\n"
        f"• ⚡ Instant Withdrawals (EasyPaisa / JazzCash / Bank)\n\n"
        f"👇 Select an option from the menu below:"
    )

    keyboard = [
        [InlineKeyboardButton("📋 Complete CPA Tasks", callback_data='tasks')],
        [InlineKeyboardButton("🎁 Daily Reward", callback_data='daily_reward'), InlineKeyboardButton("💰 My Balance", callback_data='balance')],
        [InlineKeyboardButton("💳 Withdraw", callback_data='withdraw'), InlineKeyboardButton("🔒 5-Year Vault", callback_data='vault')],
        [InlineKeyboardButton("📞 Support", url=f"https://t.me/{ADMIN_USERNAME.replace('@', '')}"), InlineKeyboardButton("📜 Privacy Policy", url=PRIVACY_URL)]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(welcome_text, parse_mode='Markdown', reply_markup=reply_markup)

async def button_click(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id

    if query.data == 'balance':
        bal = get_balance(user_id)
        text = f"💰 **Your Account Balance:**\n\n**PKRT:** {bal:.2f} PKRT\n**PKR Value:** Rs. {bal:.2f}"
        keyboard = [[InlineKeyboardButton("⬅️ Back to Menu", callback_data='main_menu')]]
        await query.edit_message_text(text, parse_mode='Markdown', reply_markup=InlineKeyboardMarkup(keyboard))

    elif query.data == 'tasks':
        text = (
            "📋 **PKRT High-Reward CPA Tasks**\n\n"
            "Niche kisi bhi task link par click karke offer complete karein aur PKRT rewards hasil karein:\n\n"
            "⚠️ **Note:** Complete tasks accurately to claim your reward balance."
        )
        keyboard = [
            [InlineKeyboardButton("📱 Task 1 Complete Karein", url=CPA_OFFER_1)],
            [InlineKeyboardButton("📱 Task 2 Complete Karein", url=CPA_OFFER_2)],
            [InlineKeyboardButton("📱 Task 3 Complete Karein", url=CPA_OFFER_3)],
            [InlineKeyboardButton("📱 Task 4 Complete Karein", url=CPA_OFFER_4)],
            [InlineKeyboardButton("📱 Task 5 Complete Karein", url=CPA_OFFER_5)],
            [InlineKeyboardButton("📱 Task 6 Complete Karein", url=CPA_OFFER_6)],
            [InlineKeyboardButton("⬅️ Back to Menu", callback_data='main_menu')]
        ]
        await query.edit_message_text(text, parse_mode='Markdown', reply_markup=InlineKeyboardMarkup(keyboard))

    elif query.data == 'daily_reward':
        add_balance(user_id, 1.0)
        await query.answer("🎁 Daily Bonus Claimed! 1.0 PKRT added.", show_alert=True)
        bal = get_balance(user_id)
        text = f"✅ **Daily Bonus Added!**\n\nNew Balance: **{bal:.2f} PKRT**"
        keyboard = [[InlineKeyboardButton("⬅️ Back to Menu", callback_data='main_menu')]]
        await query.edit_message_text(text, parse_mode='Markdown', reply_markup=InlineKeyboardMarkup(keyboard))

    elif query.data == 'withdraw':
        bal = get_balance(user_id)
        if bal < 1.0:
            text = f"⚠️ **Insufficient Balance**\n\nMinimum withdrawal is **1.00 PKRT**.\nYour Balance: **{bal:.2f} PKRT**"
        else:
            text = (
                f"💳 **Withdraw Funds**\n\n"
                f"Current Balance: **{bal:.2f} PKRT**\n\n"
                f"Send your payout details to support:\n"
                f"• EasyPaisa / JazzCash / Bank Title & Account Number\n\n"
                f"📩 Support: {ADMIN_USERNAME}"
            )
        keyboard = [[InlineKeyboardButton("⬅️ Back to Menu", callback_data='main_menu')]]
        await query.edit_message_text(text, parse_mode='Markdown', reply_markup=InlineKeyboardMarkup(keyboard))

    elif query.data == 'vault':
        text = (
            "🔒 **PKRT 5-Year Vault Lock**\n\n"
            "Lock your PKRT tokens for 5 years to target a **1:1 USDT** exchange value parity.\n\n"
            "Contact admin to enter the long-term vault program."
        )
        keyboard = [
            [InlineKeyboardButton("📩 Contact Admin", url=f"https://t.me/{ADMIN_USERNAME.replace('@', '')}")],
            [InlineKeyboardButton("⬅️ Back to Menu", callback_data='main_menu')]
        ]
        await query.edit_message_text(text, parse_mode='Markdown', reply_markup=InlineKeyboardMarkup(keyboard))

    elif query.data == 'main_menu':
        user = query.from_user
        welcome_text = (
            f"🇵🇰 **PKRT Official Ecosystem** 🇵🇰\n\n"
            f"📊 **Base Value:** 1 PKRT = 1 PKR\n"
            f"💸 **Minimum Cashout:** 1.00 PKRT\n\n"
            f"👇 Select an option from the menu:"
        )
        keyboard = [
            [InlineKeyboardButton("📋 Complete CPA Tasks", callback_data='tasks')],
            [InlineKeyboardButton("🎁 Daily Reward", callback_data='daily_reward'), InlineKeyboardButton("💰 My Balance", callback_data='balance')],
            [InlineKeyboardButton("💳 Withdraw", callback_data='withdraw'), InlineKeyboardButton("🔒 5-Year Vault", callback_data='vault')],
            [InlineKeyboardButton("📞 Support", url=f"https://t.me/{ADMIN_USERNAME.replace('@', '')}"), InlineKeyboardButton("📜 Privacy Policy", url=PRIVACY_URL)]
        ]
        await query.edit_message_text(welcome_text, parse_mode='Markdown', reply_markup=InlineKeyboardMarkup(keyboard))

def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_click))

    print("PKRT Official Bot is running successfully...")
    app.run_polling()

if __name__ == '__main__':
    main()
      
