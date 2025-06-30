import random
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, CallbackQueryHandler

TOKEN = "токен"

HOROSCOPES = {
    "овен": [
        "♈ Овен\nСегодня ты найдёшь баг, который все пропустили. Не радуйся слишком громко — девопс уже плачет."
    ],
    "телец": [
        "♉ Телец\nДень стабильный, как билд после 7 фиксов. Главное — не залипни в одном тест-кейсе на 3 часа."
    ],
    "близнецы": [
        "♊ Близнецы\nТы напишешь баг-репорт, сам его закроешь, а потом откроешь снова. Всё как обычно."
    ],
    "рак": [
        "♋ Рак\nСегодня баги будут тебя обижать. Не бери близко к сердцу — это просто код, не люди."
    ],
    "лев": [
        "♌ Лев\nВремя заявить о себе: громко находи баги и ещё громче про них рассказывай. Только не забудь их задокументировать!"
    ],
    "дева": [
        "♍ Дева\nСегодня твой баг-репорт отправят в учебник по тестированию. Но всё равно его закроют как 'won't fix'."
    ],
    "весы": [
        "♎ Весы\nТы 20 минут будешь выбирать, какой severity поставить. Просто выбери 'Medium' — не ошибёшься."
    ],
    "скорпион": [
        "♏ Скорпион\nЧувствуешь, где баг? Иди туда. Разработчик будет отрицать, но ты всё равно окажешься прав."
    ],
    "стрелец": [
        "♐ Стрелец\nТестируй с азартом, но не забывай: 'на проде' — не площадка для экспериментов. Или... ну ты понял."
    ],
    "козерог": [
        "♑ Козерог\nСегодня ты закроешь все задачи и начнёшь чужие. Команда в шоке, ты — доволен."
    ],
    "водолей": [
        "♒ Водолей\nСлучайно найдёшь баг в фиче, которую ещё не начали пилить. Коллеги будут называть тебя пророком."
    ],
    "рыбы": [
        "♓ Рыбы\nСегодня ты почувствуешь баг ещё до запуска приложения. Доверься чуйке — она тебя не подводила."
    ]
}

def get_zodiac_keyboard():
    keyboard = [
        [
            InlineKeyboardButton("♈ Овен", callback_data="овен"),
            InlineKeyboardButton("♉ Телец", callback_data="телец"),
            InlineKeyboardButton("♊ Близнецы", callback_data="близнецы"),
        ],
        [
            InlineKeyboardButton("♋ Рак", callback_data="рак"),
            InlineKeyboardButton("♌ Лев", callback_data="лев"),
            InlineKeyboardButton("♍ Дева", callback_data="дева"),
        ],
        [
            InlineKeyboardButton("♎ Весы", callback_data="весы"),
            InlineKeyboardButton("♏ Скорпион", callback_data="скорпион"),
            InlineKeyboardButton("♐ Стрелец", callback_data="стрелец"),
        ],
        [
            InlineKeyboardButton("♑ Козерог", callback_data="козерог"),
            InlineKeyboardButton("♒ Водолей", callback_data="водолей"),
            InlineKeyboardButton("♓ Рыбы", callback_data="рыбы"),
        ]
    ]
    return InlineKeyboardMarkup(keyboard)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Отправка локальной картинки
    with open('welcome.jpg', 'rb') as photo:
        await update.message.reply_photo(
            photo=photo,
            caption="🔮 *QA-гороскоп на сегодня!*\n\n"
                    "Узнай, что звёзды приготовили для твоего тестирования ✨",
            parse_mode="Markdown"
        )

    # Отправка кнопок (один раз)
    await update.message.reply_text(
        "👇 Выбирай знак зодиака:",
        reply_markup=get_zodiac_keyboard()
    )

async def handle_zodiac_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    zodiac = query.data
    prediction = HOROSCOPES[zodiac][0]
    await query.edit_message_text(
        f"{prediction}\n\nХочешь другой знак? Выбирай:",
        reply_markup=get_zodiac_keyboard()
    )

def main():
    application = ApplicationBuilder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(handle_zodiac_button))
    print("Бот запущен! Нажмите Ctrl+C для остановки.")
    application.run_polling()

if __name__ == "__main__":
    main()
