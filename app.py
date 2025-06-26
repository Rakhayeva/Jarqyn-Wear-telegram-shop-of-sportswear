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
        await query.message.reply_photo(photo=open("images/AgACAgIAAxkBAAMSaF1QI9J6v6jUdkIm11yd5z-TfT4AAu_uMRuTdehK-NxYzJdGMOUBAAMCAAN4AAM2BA.jpg", "rb"))
        color_keyboard = [
            [InlineKeyboardButton("Белый", callback_data="color_secure_white")],
            [InlineKeyboardButton("Голубой", callback_data="color_secure_blue")],
            [InlineKeyboardButton("Черный", callback_data="color_secure_black")]
        ]
        size_keyboard = [
            [InlineKeyboardButton("S", callback_data="size_secure_S"), InlineKeyboardButton("M", callback_data="size_secure_M"), InlineKeyboardButton("L", callback_data="size_secure_L")]
        ]
    elif model == "bra_active":
        await query.message.reply_photo(photo=open("images/AgACAgIAAxkBAAMZaF1QkZBN1U7qGFCId_DcwBZ88XoAAlr0MRu9IOlKJlKv6ea526MBAAMCAAN5AAM2BA.jpg", "rb"))
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

# Обработка выбора цвета для моделей бра
async def color_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    color = query.data

    # Для модели bra_secure
    if color == "color_secure_white":
        await query.message.reply_photo(photo="AgACAgIAAxkBAAMSaF1QI9J6v6jUdkIm11yd5z-TfT4AAu_uMRuTdehK-NxYzJdGMOUBAAMCAAN4AAM2BA")
    elif color == "color_secure_blue":
        await query.message.reply_photo(photo="AgACAgIAAxkBAAMVaF1QV5C8Xlzqweezwtf2OCkMPSgAAvLuMRuTdehKSgviwXX4618BAAMCAAN4AAM2BA")
    elif color == "color_secure_black":
        await query.message.reply_photo(photo="AgACAgIAAxkBAAMXaF1QcIuVJTKkyKQjXGOxAAFBv-mJAALz7jEbk3XoSg88Ty4NENp5AQADAgADeAADNgQ")

    # Для модели bra_active
    elif color == "color_active_white":
    photos = [
        InputMediaPhoto(media="AgACAgIAAxkBAAMbaF1SgjEkYFRhRaKjPTsd74_KZRkAAmj0MRu9IOlKgpnzRQ8-LpMBAAMCAAN5AAM2BA"),
        InputMediaPhoto(media="fileAgACAgIAAxkBAAMdaF1SjxSotsnyF7W7sKRHdWLra4cAAmr0MRu9IOlKTo8e3zTlKocBAAMCAAN5AAM2BA_id_2"),
    ]
    await query.message.reply_media_group(photos)
    
    elif color == "color_active_blue":
        photos = [
        InputMediaPhoto(media="AgACAgIAAxkBAAMZaF1QkZBN1U7qGFCId_DcwBZ88XoAAlr0MRu9IOlKJlKv6ea526MBAAMCAAN5AAM2BA"),
        InputMediaPhoto(media="AgACAgIAAxkBAAMfaF1TFtF5PkVRfrgtkMfqLOh8kh8AAm30MRu9IOlK8PNQrrTOZyUBAAMCAAN5AAM2BA"),
    ]
    await query.message.reply_media_group(photos)

    elif color == "color_active_mint":
        photos = [
        InputMediaPhoto(media="AgACAgIAAxkBAAMhaF1TckEINY4B6LOS_Eg2UeYMfzkAAm_0MRu9IOlKLUVxz6Z4RM0BAAMCAAN5AAM2BA"),
        InputMediaPhoto(media="AgACAgIAAxkBAAMjaF1Tks1dTxCPELimRvpgLd5BgcUAArj9MRsdF-hKq8Wb0ks8a1UBAAMCAAN5AAM2BA"),
    ]
    await query.message.reply_media_group(photos)

    elif color == "color_active_black":
        photos = [
        InputMediaPhoto(media="AgACAgIAAxkBAAMlaF1T0dqffe_UjoLWY6La1MZYbSUAAnT0MRu9IOlKtBcsjaj4FboBAAMCAAN5AAM2BA"),
        InputMediaPhoto(media="AgACAgIAAxkBAAMnaF1T2A9YJk3hTqjZqHCCpGQvwzYAAiHvMRuTdehKml9did1WGr0BAAMCAAN5AAM2BA"),
    ]
    await query.message.reply_media_group(photos)


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
    app.add_handler(CallbackQueryHandler(bra_model_handler, pattern="^bra_.*$"))
    app.add_handler(CallbackQueryHandler(color_handler, pattern="^color_.*$")) 

    app.run_polling()

if __name__ == "__main__":
    main()

