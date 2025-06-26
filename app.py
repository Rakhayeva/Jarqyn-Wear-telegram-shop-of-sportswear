import os
from telegram import (
    Update, InlineKeyboardButton, InlineKeyboardMarkup,
    ReplyKeyboardMarkup, InputMediaPhoto
)
from telegram.ext import (
    Application, CommandHandler, CallbackQueryHandler,
    MessageHandler, ContextTypes, filters
)

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

async def show_catalog(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("Бра", callback_data="cat_bra")],
        [InlineKeyboardButton("Лосины", callback_data="cat_leggings")],
        [InlineKeyboardButton("Футболки", callback_data="cat_tshirts")],
        [InlineKeyboardButton("Майки", callback_data="cat_tanks")],
        [InlineKeyboardButton("Лонгсливы", callback_data="cat_longsleeves")],
        [InlineKeyboardButton("Носки", callback_data="cat_socks")],
        [InlineKeyboardButton("Нижнее белье", callback_data="cat_underwear")]
    ]
    await update.message.reply_text("Выбери категорию:", reply_markup=InlineKeyboardMarkup(keyboard))

# Заглушка для категории
async def category_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    cat_map = {
        "cat_bra": "Бра",
        "cat_leggings": "Лосины",
        "cat_tshirts": "Футболки",
        "cat_tanks": "Майки",
        "cat_longsleeves": "Лонгсливы",
        "cat_socks": "Носки",
        "cat_underwear": "Нижнее белье"
    }
    category = cat_map.get(query.data, "Категория")
    await query.edit_message_text(f"В категории {category} скоро появятся товары 👀")

# Контакты
async def contacts(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📞 Напишите нам в WhatsApp:\nhttps://wa.me/77052963629")

# О нас
async def about(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Стильная и надёжная эстетика спорта по честной цене. Для девушек и женщин, которые заботятся о себе и выбирают удобство.")

def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & filters.Regex("Каталог"), show_catalog))
    app.add_handler(MessageHandler(filters.TEXT & filters.Regex("Контакты"), contacts))
    app.add_handler(MessageHandler(filters.TEXT & filters.Regex("О нас"), about))

    app.add_handler(CallbackQueryHandler(category_handler, pattern="^cat_.*$"))

    app.run_polling()

if __name__ == "__main__":
    main()

