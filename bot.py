import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

BOT_TOKEN = os.getenv('BOT_TOKEN')
ADMIN_ID = 6540509823  # ЗАМЕНИТЕ НА ВАШ РЕАЛЬНЫЙ ID

async def start(update: Update, context: CallbackContext):
    user = update.effective_user
    
    keyboard = [
        [InlineKeyboardButton("🎁 Магазин NFT", callback_data="shop")],
        [InlineKeyboardButton("💼 Мои сделки", callback_data="trades")],
    ]
    
    # Добавляем админ кнопку если это админ
    if user.id == ADMIN_ID:
        keyboard.append([InlineKeyboardButton("🛠️ Админ панель", callback_data="admin")])
    
    await update.message.reply_text(
        f"👋 Привет, {user.first_name}!\n\n"
        "Добро пожаловать в бота для сделок с NFT!",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def admin_panel(update: Update, context: CallbackContext):
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

async def button_handler(update: Update, context: CallbackContext):
    query = update.callback_query
    
    if query.data == "admin":
        await admin_panel(update, context)
    elif query.data == "back":
        await start(update, context)
    else:
        await query.message.edit_text("⚙️ Функция в разработке...")

def main():
    if not BOT_TOKEN:
        print("❌ ОШИБКА: BOT_TOKEN не найден!")
        return
    
    # Создаем updater и передаем ему токен бота
    updater = Updater(BOT_TOKEN)
    
    # Получаем диспетчер для регистрации обработчиков
    dispatcher = updater.dispatcher
    
    # Регистрируем обработчики команд
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CallbackQueryHandler(button_handler))
    
    # Запускаем бота
    print("🤖 Бот запускается...")
    updater.start_polling()
    print("✅ Бот успешно запущен!")
    
    # Запускаем бота до тех пор, пока пользователь не остановит его
    updater.idle()

if __name__ == "__main__":
    main()