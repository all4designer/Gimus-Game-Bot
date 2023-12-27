from db import *

questions = [
    "Ты когда-нибудь был за границей?",
    "Пробовал ли ты экзотическую еду?",
    "Ты когда-нибудь прыгал с тарзанкой?",
    "Был ли ты на концерте твоей любимой группы?",
    "Испытывал ли ты страх высоты?",
    "Встречался ли ты когда-нибудь с знаменитостью?",
    "Пробовал ли ты научиться новому виду спорта?",
    "Был ли ты на велосипедной прогулке в горах?",
    "Имел ли ты опыт вождения спортивного автомобиля?",
    "Пробовал ли ты готовить блюда из другой культуры?"
]

actions = [
    "Станцуй под любимую мелодию на месте",
    "Сыграй на музыкальном инструменте, если у тебя он есть",
    "Попробуй сделать разворот на месте, как водитель такси",
    "Нарисуй портрет одного из присутствующих за 2 минуты",
    "Прочитай вслух отрывок из любимой книги или стихотворение",
    "Зажги свечу и покажи свой танец светлячка",
    "Сыграй вспышечную игру: сделай наиболее смешную фотографию",
    "Сыграй мини-пьесу, используя любые предметы в комнате в качестве костюмов и декораций",
    "Организуй стендап и расскажи шутку",
    "Поделись самой смешной историей из своей жизни"
]
@dp.callback_query_handler(lambda c: c.data in ['pravda', 'new_pravda'])
async def pravda(callback_query: types.CallbackQuery):
    message_id = callback_query.message.message_id
    user_id = callback_query.from_user.id
    data = callback_query.data

    if data == 'new_pravda':
        await win(user_id, 'pravda')

    keyboard = InlineKeyboardMarkup(row_width=2)
    buttons = [InlineKeyboardButton('🪬 Правда', callback_data='truth'),
               InlineKeyboardButton('🍄 Действие', callback_data='action'),
               InlineKeyboardButton('🔙 Назад в меню', callback_data='start'),
    ]
    keyboard.add(*buttons)

    await bot.edit_message_media(chat_id=user_id,
                                 message_id=message_id,
                                 media=types.InputMediaPhoto(media=open('pravda.jpg', 'rb'),
                                 caption="<b>Собери своих друзей рядом.</b>\n\nПо очереди нажимайте на кнопки с правдой или действием:",
                                 parse_mode='HTML'),
                                 reply_markup=keyboard
    )
@dp.callback_query_handler(lambda c: c.data in ['truth', 'action'])
async def get_question_or_action(callback_query: types.CallbackQuery):
    message_id = callback_query.message.message_id
    user_id = callback_query.from_user.id
    data = callback_query.data

    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(InlineKeyboardButton('✅ Задание выполнено', callback_data='new_pravda'),
                 InlineKeyboardButton('🔙 Назад в меню', callback_data='start'))

    if data == 'truth':
        text = random.choice(questions)
    elif data == 'action':
        text = random.choice(actions)
    await bot.edit_message_media(chat_id=user_id,
                                 message_id=message_id,
                                 media=types.InputMediaPhoto(media=open('pravda.jpg', 'rb'),
                                                             caption=f"{text}",
                                                             parse_mode='HTML'),
                                 reply_markup=keyboard
                                 )