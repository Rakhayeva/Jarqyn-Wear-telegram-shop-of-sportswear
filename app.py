import os
from telegram import Update
from telegram import ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters

# Получаем токен из переменной окружения (безопасно)
BOT_TOKEN = os.environ.get("BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        ["📋 Каталог", "🛒 Корзина"],
        ["ℹ️ О нас", "📞 Контакты"]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

    await update.message.reply_text(
        "Привет 👋 Добро пожаловать в Jarqyn Wear — магазин стильной и доступной одежды для спорта и йоги!\n\n"
        "Выбери действие ниже:",
        reply_markup=reply_markup
    )

# Обработчик кнопки 📋 Каталог
async def show_catalog(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Вот наш каталог 🛍️:\n(позже сюда добавим список товаров)")

def main():
    app = Application.builder().token(BOT_TOKEN).build()

    # Обработчики
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & filters.Regex("📋 Каталог"), show_catalog))

    # Запуск бота
    app.run_polling()

if __name__ == "__main__":
    main()