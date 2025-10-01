import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

BOT_TOKEN = os.getenv('BOT_TOKEN', 'your_bot_token_here')

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    
    keyboard = [
        [InlineKeyboardButton("🎁 Магазин NFT", callback_data="shop")],
        [InlineKeyboardButton("💼 Мои сделки", callback_data="trades")],
    ]
    
    # Добавляем админ кнопку если это админ
    if user.id == 6540509823:  # ЗАМЕНИТЕ НА ВАШ ID
        keyboard.append([InlineKeyboardButton("🛠️ Админ панель", callback_data="admin")])
    
    await update.message.reply_text(
        f"👋 Привет, {user.first_name}!\n\n"
        "Добро пожаловать в бота для сделок с NFT!",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def admin_panel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    
    keyboard = [
        [InlineKeyboardButton("📊 Статистика", callback_data="stats")],
        [InlineKeyboardButton("🎁 Управление NFT", callback_data="manage_nft")],
        [InlineKeyboardButton("🔙 Назад", callback_data="back")]
    ]
    
    await query.message.edit_text(
        "🛠️ **Панель администратора**\n\n"
        "📊 Ваша статистика:\n"
        "• Сделок: 1423\n"
        "• Рейтинг: 5.0/5 ⭐⭐⭐⭐⭐\n"
        "💎 Баланс: Безлимитный",
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode='Markdown'
    )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    
    if query.data == "admin":
        await admin_panel(update, context)
    elif query.data == "back":
        await start(update, context)
    else:
        await query.message.edit_text("⚙️ Функция в разработке...")

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    
    print("🤖 Бот запущен!")
    app.run_polling()

if name == "__main__":
    main()
