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
ADMIN_ID = 123456789  # ЗАМЕНИТЕ НА ВАШ РЕАЛЬНЫЙ ID

def start(update: Update, context: CallbackContext):
    user = update.effective_user
    
    keyboard = [
        [InlineKeyboardButton("🎁 Магазин NFT", callback_data="shop")],
        [InlineKeyboardButton("💼 Мои сделки", callback_data="trades")],
    ]
    
    # Добавляем админ кнопку если это админ
    if user.id == ADMIN_ID:
        keyboard.append([InlineKeyboardButton("🛠️ Админ панель", callback_data="admin")])
    
    update.message.reply_text(
        f"👋 Привет, {user.first_name}!\n\n"
        "Добро пожаловать в бота для сделок с NFT!",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

def admin_panel(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    
    keyboard = [
        [InlineKeyboardButton("📊 Статистика", callback_data="stats")],
        [InlineKeyboardButton("🎁 Управление NFT", callback_data="manage_nft")],
        [InlineKeyboardButton("👥 Пользователи", callback_data="admin_users")],
        [InlineKeyboardButton("🔙 Главное меню", callback_data="main_menu")]
    ]
    
    query.edit_message_text(
        "🛠️ *Панель администратора*\n\n"
        "📊 Ваша статистика:\n"
        "• Сделок: 1423\n"
        "• Рейтинг: 5.0/5 ⭐⭐⭐⭐⭐\n"
        "💎 Баланс: Безлимитный\n\n"
        "Выберите действие:",
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode='Markdown'
    )

def admin_stats(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    
    stats_text = (
        "📊 *Статистика системы*\n\n"
        "👥 Пользователей: `15`\n"
        "🎁 NFT товаров: `7`\n"
        "💼 Активных сделок: `3`\n"
        "💎 Ваш статус: *АДМИНИСТРАТОР*\n\n"
        "🛠️ Управление через админ панель"
    )
    
    keyboard = [[InlineKeyboardButton("🔙 Назад", callback_data="admin_panel")]]
    query.edit_message_text(stats_text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='Markdown')

def button_handler(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    
    if query.data == "admin":
        admin_panel(update, context)
    elif query.data == "admin_panel":
        admin_panel(update, context)
    elif query.data == "stats":
        admin_stats(update, context)
    elif query.data == "main_menu":
        start(update, context)
    else:
        query.edit_message_text("⚙️ Функция в разработке...")

def test_command(update: Update, context: CallbackContext):
    update.message.reply_text("✅ Тестовая команда работает!")

def main():
    if not BOT_TOKEN:
        print("❌ ОШИБКА: BOT_TOKEN не найден!")
        print("✅ Убедитесь что переменная BOT_TOKEN установлена в Render")
        return
    
    # Создаем Updater
    updater = Updater(BOT_TOKEN, use_context=True)
    
    # Получаем диспетчер
    dp = updater.dispatcher
    
    # Регистрируем обработчики
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("test", test_command))
    dp.add_handler(CallbackQueryHandler(button_handler))
    
    # Запускаем бота
    print("🤖 Бот запускается...")
    print(f"✅ Токен получен: {BOT_TOKEN[:10]}...")
    
    updater.start_polling()
    print("✅ Бот успешно запущен!")
    
    # Бот работает до принудительной остановки
    updater.idle()

if __name__ == "__main__":
    main()

    
    
    