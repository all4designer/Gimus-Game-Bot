from db import *

questions = [
    {
        'question': 'Сколько планет в Солнечной системе?',
        'options': ['7', '8', '9', '10'],
        'correct_answer': '8'
    },
    {
        'question': 'Какое самое высокое здание в мире?',
        'options': ['Шанхайская башня', 'Эйфелева башня', 'Бурдж-Халифа', 'Лондонский мост'],
        'correct_answer': 'Бурдж-Халифа'
    },
    {
        'question': 'Кто написал "Войну и мир"?',
        'options': ['Федор Достоевский', 'Лев Толстой', 'Иван Тургенев', 'Александр Пушкин'],
        'correct_answer': 'Лев Толстой'
    },
    {
        'question': 'Как называется столица Франции?',
        'options': ['Лондон', 'Мадрид', 'Париж', 'Рим'],
        'correct_answer': 'Париж'
    },
    {
        'question': 'Что представляет собой бинарный код?',
        'options': ['Система исчисления с основанием 10', 'Язык программирования', 'Система исчисления с основанием 2', 'Способ кодирования текста'],
        'correct_answer': 'Система исчисления с основанием 2'
    },
    {
        'question': 'Кто изобрел телефон?',
        'options': ['Томас Эдисон', 'Никола Тесла', 'Александр Грамбелль', 'Александр Белл'],
        'correct_answer': 'Александр Белл'
    },
    {
        'question': 'Какой химический элемент обозначается символом "Fe"?',
        'options': ['Фосфор', 'Железо', 'Фтор', 'Франций'],
        'correct_answer': 'Железо'
    },
    {
        'question': 'Кто написал "Гамлета"?',
        'options': ['Уильям Шекспир', 'Джейн Остин', 'Федор Достоевский', 'Марк Твен'],
        'correct_answer': 'Уильям Шекспир'
    },
    {
        'question': 'Какой океан самый большой по площади?',
        'options': ['Тихий', 'Атлантический', 'Индийский', 'Северный Ледовитый'],
        'correct_answer': 'Тихий'
    },
    {
        'question': 'Как называется самая длинная река в мире?',
        'options': ['Нил', 'Амазонка', 'Миссисипи', 'Янцзы'],
        'correct_answer': 'Амазонка'
    },
]

@dp.callback_query_handler(lambda c: c.data == 'megatest')
async def megatest(callback_query: types.CallbackQuery):
    message_id = callback_query.message.message_id
    chat_id = callback_query.from_user.id

    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton('🆕 Новая игра', callback_data='start_megatest'))
    keyboard.add(InlineKeyboardButton('🔙 Назад в меню', callback_data='start'))

    await bot.edit_message_media(chat_id=chat_id,
                                 message_id=message_id,
                                 media=types.InputMediaPhoto(media=open('megatest.jpg', 'rb'),
                                 caption="<b>Готов проверить свой интеллект?</b>\n\nЯ буду задавать тебе вопросы, твоя задача правильно на них отвечать.\n\nНачинай новую игру:",
                                 parse_mode='HTML'),
                                 reply_markup=keyboard
    )
@dp.callback_query_handler(lambda c: c.data == 'start_megatest')
async def start_megatest(callback_query: types.CallbackQuery):
    message_id = callback_query.message.message_id
    chat_id = callback_query.from_user.id

    random_question = random.choice(questions)
    question_text = random_question['question']
    options = random_question['options']
    correct_answer = random_question['correct_answer']

    keyboard = InlineKeyboardMarkup(row_width=2)
    for option in options:
        callback_data = f"{option}+{correct_answer}" if option == correct_answer else f"{option}+"
        keyboard.add(InlineKeyboardButton(option, callback_data=callback_data))
    keyboard.add(InlineKeyboardButton('🔙 Назад в меню', callback_data='start'))

    await bot.edit_message_media(chat_id=chat_id,
                                 message_id=message_id,
                                 media=types.InputMediaPhoto(media=open('megatest.jpg', 'rb'),
                                 caption=f"<b>{question_text}</b>",
                                 parse_mode='HTML'),
                                 reply_markup=keyboard
    )


@dp.callback_query_handler(lambda c: '+' in c.data)
async def check_correct_answer(callback_query: types.CallbackQuery):
    option, correct_answer = callback_query.data.split('+')
    message_id = callback_query.message.message_id
    user_id = callback_query.from_user.id

    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton('🆕 Новая игра', callback_data='start_megatest'))
    keyboard.add(InlineKeyboardButton('🔙 Назад в меню', callback_data='start'))

    if option == correct_answer:
        text = '<b>Поздравляю, ты угадал!</b>\n\nЧто делаем дальше?'
        await win(user_id, 'megatest')
    else:
        text = '<b>Ты не угадал!</b>\n\nЧто делаем дальше?'

    await bot.edit_message_media(chat_id=user_id,
                                     message_id=message_id,
                                     media=types.InputMediaPhoto(media=open('megatest.jpg', 'rb'),
                                     caption=text,
                                     parse_mode='HTML'),
                                     reply_markup=keyboard
        )