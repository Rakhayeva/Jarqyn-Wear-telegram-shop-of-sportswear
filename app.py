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

# Опции товара после выбора категории
async def category_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "cat_bra":
        keyboard = [
            [InlineKeyboardButton("Бра Secure Support", callback_data="bra_secure")],
            [InlineKeyboardButton("Бра Active Move", callback_data="bra_active")]
        ]
        await query.edit_message_text("Выбери модель бра:", reply_markup=InlineKeyboardMarkup(keyboard))

    # Можно будет добавить аналогично для других категорий


# Опции для моделей бра
async def bra_model_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    model = query.data
    color_keyboard = []
    size_keyboard = []
    chart_button = InlineKeyboardButton("📐 Таблица размеров", callback_data=f"{model}_chart")


    if model == "bra_secure":
        # Показываем фото модели
        await query.message.reply_photo(photo=open("images/bra_secure_support.jpg", "rb"))
        color_keyboard = [
            [InlineKeyboardButton("Белый", callback_data="color_secure_white")],
            [InlineKeyboardButton("Голубой", callback_data="color_secure_blue")],
            [InlineKeyboardButton("Черный", callback_data="color_secure_black")]
        ]
        size_keyboard = [
            [InlineKeyboardButton("S", callback_data="size_secure_S"), InlineKeyboardButton("M", callback_data="size_secure_M"), InlineKeyboardButton("L", callback_data="size_secure_L")]
        ]
    elif model == "bra_active":
        await query.message.reply_photo(photo=open("images/bra_active_move.jpg", "rb"))
        color_keyboard = [
            [InlineKeyboardButton("Белый", callback_data="color_active_white")],
            [InlineKeyboardButton("Голубой", callback_data="color_active_blue")],
            [InlineKeyboardButton("Мятный", callback_data="color_active_mint")],
            [InlineKeyboardButton("Черный", callback_data="color_active_black")]
        ]
        size_keyboard = [
            [InlineKeyboardButton("S", callback_data="size_active_S"), InlineKeyboardButton("M", callback_data="size_active_M"),
             InlineKeyboardButton("L", callback_data="size_active_L"), InlineKeyboardButton("XL", callback_data="size_active_XL")]
        ]

    await query.message.reply_text("Выберите цвет:", reply_markup=InlineKeyboardMarkup(color_keyboard))
    await query.message.reply_text("Выберите размер:", reply_markup=InlineKeyboardMarkup(size_keyboard))
    await query.message.reply_text("Дополнительно:", reply_markup=InlineKeyboardMarkup([[chart_button]]))



# Контакты
async def contacts(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📞 Напишите нам в WhatsApp:\nhttps://wa.me/77052963629")

# О нас
async def about(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Стильная и надёжная эстетика спорта по честной цене. Для девушек и женщин, которые заботятся о себе и выбирают удобство.")

# Логгер для получения file_id фотографий
async def photo_logger(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.photo:
        file_id = update.message.photo[-1].file_id
        await update.message.reply_text(f"🆔 file_id: {file_id}")

def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & filters.Regex("Каталог"), show_catalog))
    app.add_handler(MessageHandler(filters.TEXT & filters.Regex("Контакты"), contacts))
    app.add_handler(MessageHandler(filters.TEXT & filters.Regex("О нас"), about))
    app.add_handler(MessageHandler(filters.PHOTO, photo_logger))


    app.add_handler(CallbackQueryHandler(category_handler, pattern="^cat_.*$"))

    app.run_polling()

if __name__ == "__main__":
    main()

