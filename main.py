import logging
from threading import Thread
from flask import Flask
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# 🌐 24/7 Web Server Setup
app_web = Flask('')

@app_web.route('/')
def home():
    return "PKRT Bot Active 24/7"

def run_web():
    app_web.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run_web)
    t.start()

# 🇵🇰 Configuration -
BOT_TOKEN = "8878827364:AAHk-sX2zvipBvkwukaW83Y-ht-S-2e8tbg"
ADMIN_USERNAME = "@PKRTsupport"
PRIVACY_URL = "https://telegra.ph/PKRT-Official-Ecosystem---Privacy-Policy-08-31"

# CPA Offer Links
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
        f"👇 Select an option from the menu below:"
    )

    keyboard = [
        [InlineKeyboardButton("🛒 Buy PKRT Coins", callback_data='buy_coins'), InlineKeyboardButton("📋 CPA Tasks", callback_data='tasks')],
        [InlineKeyboardButton("🎁 Daily Reward", callback_data='daily_reward'), InlineKeyboardButton("💰 My Balance", callback_data='balance')],
        [InlineKeyboardButton("💳 Withdraw", callback_data='withdraw'), InlineKeyboardButton("🔒 5-Year Vault", callback_data='vault')],
        [InlineKeyboardButton("📞 Support", url=f"https://t.me/{ADMIN_USERNAME.replace('@', '')}"), InlineKeyboardButton("📜 Privacy Policy", url=PRIVACY_URL)]
    ]
    await update.message.reply_text(welcome_text, parse_mode='Markdown', reply_markup=InlineKeyboardMarkup(keyboard))

async def button_click(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id

    if query.data == 'buy_coins':
        text = (
            "🛒 **Buy PKRT Coins (Official Rates)**\n\n"
            "• **Price:** 1 PKRT = Rs. 1 PKR\n"
            "• **Payment Methods:** EasyPaisa / JazzCash / Bank Transfer\n\n"
            "Aap jitne coins buy karna chahte hain, direct Admin ko message karke payment sending detail hasil karein:\n\n"
            f"📩 **Contact Admin:** {ADMIN_USERNAME}"
        )
        keyboard = [
            [InlineKeyboardButton("💬 Buy via Admin", url=f"https://t.me/{ADMIN_USERNAME.replace('@', '')}")],
            [InlineKeyboardButton("⬅️ Back to Menu", callback_data='main_menu')]
        ]
        await query.edit_message_text(text, parse_mode='Markdown', reply_markup=InlineKeyboardMarkup(keyboard))

    elif query.data == 'balance':
        bal = get_balance(user_id)
        text = f"💰 **Your Balance:** {bal:.2f} PKRT"
        keyboard = [[InlineKeyboardButton("⬅️ Back to Menu", callback_data='main_menu')]]
        await query.edit_message_text(text, parse_mode='Markdown', reply_markup=InlineKeyboardMarkup(keyboard))

    elif query.data == 'tasks':
        text = "📋 **PKRT High-Reward CPA Tasks:**"
        keyboard = [
            [InlineKeyboardButton("📱 Task 1 Complete", url=CPA_OFFER_1)],
            [InlineKeyboardButton("📱 Task 2 Complete", url=CPA_OFFER_2)],
            [InlineKeyboardButton("📱 Task 3 Complete", url=CPA_OFFER_3)],
            [InlineKeyboardButton("📱 Task 4 Complete", url=CPA_OFFER_4)],
            [InlineKeyboardButton("📱 Task 5 Complete", url=CPA_OFFER_5)],
            [InlineKeyboardButton("📱 Task 6 Complete", url=CPA_OFFER_6)],
            [InlineKeyboardButton("⬅️ Back to Menu", callback_data='main_menu')]
        ]
        await query.edit_message_text(text, parse_mode='Markdown', reply_markup=InlineKeyboardMarkup(keyboard))

    elif query.data == 'daily_reward':
        add_balance(user_id, 1.0)
        await query.answer("🎁 Daily Bonus Added!", show_alert=True)
        bal = get_balance(user_id)
        text = f"✅ **Bonus Added!**\nBalance: **{bal:.2f} PKRT**"
        keyboard = [[InlineKeyboardButton("⬅️ Back to Menu", callback_data='main_menu')]]
        await query.edit_message_text(text, parse_mode='Markdown', reply_markup=InlineKeyboardMarkup(keyboard))

    elif query.data == 'withdraw':
        bal = get_balance(user_id)
        text = f"💳 **Withdraw Funds**\n\nBalance: **{bal:.2f} PKRT**\n\nContact support: {ADMIN_USERNAME}"
        keyboard = [[InlineKeyboardButton("⬅️ Back to Menu", callback_data='main_menu')]]
        await query.edit_message_text(text, parse_mode='Markdown', reply_markup=InlineKeyboardMarkup(keyboard))

    elif query.data == 'vault':
        text = "🔒 **PKRT 5-Year Vault**\n\nTarget parity: 1 USDT.\nContact admin to participate."
        keyboard = [
            [InlineKeyboardButton("📩 Contact Admin", url=f"https://t.me/{ADMIN_USERNAME.replace('@', '')}")],
            [InlineKeyboardButton("⬅️ Back to Menu", callback_data='main_menu')]
        ]
        await query.edit_message_text(text, parse_mode='Markdown', reply_markup=InlineKeyboardMarkup(keyboard))

    elif query.data == 'main_menu':
        welcome_text = "🇵🇰 **PKRT Official Ecosystem** 🇵🇰\n\nSelect an option:"
        keyboard = [
            [InlineKeyboardButton("🛒 Buy PKRT Coins", callback_data='buy_coins'), InlineKeyboardButton("📋 CPA Tasks", callback_data='tasks')],
            [InlineKeyboardButton("🎁 Daily Reward", callback_data='daily_reward'), InlineKeyboardButton("💰 My Balance", callback_data='balance')],
            [InlineKeyboardButton("💳 Withdraw", callback_data='withdraw'), InlineKeyboardButton("🔒 5-Year Vault", callback_data='vault')],
            [InlineKeyboardButton("📞 Support", url=f"https://t.me/{ADMIN_USERNAME.replace('@', '')}"), InlineKeyboardButton("📜 Privacy Policy", url=PRIVACY_URL)]
        ]
        await query.edit_message_text(welcome_text, parse_mode='Markdown', reply_markup=InlineKeyboardMarkup(keyboard))

def main():
    keep_alive()
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_click))
    print("Bot Running...")
    app.run_polling()

if __name__ == '__main__':
    main()
