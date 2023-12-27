from db import *

movies = {
    "Звездные войны": "🌌👽🚀",
    "Терминатор": "🤖🔫⚔",
    "Матрица": "🕶💊🤖",
    "Крепкий орешек": "🏙🔫💣",
    "Назад в будущее": "⏰🚗⚡",
    "Побег из Шоушенка": "🔒🔨📜",
    "Сияние": "🏨❄👦",
    "Крестный отец": "🤵🔫",
    "В бой идут одни 'старики'": "🚜💣🍅",
    "Список Шиндлера": "📜❤️",
    "Храброе сердце": "💙󠁧󠁢󠁳󠁣󠁴⚔👑",
    "Пираты Карибского моря": "☠⚔🌊",
    "Гладиатор": "⚔👑🏛",
    "Интерстеллар": "🚀⏳🕳",
    "Достучаться до небес": "🥊👼🍻"
}
async def generate_movie_image(movie):
    emoji = movies.get(movie)
    image = Image.open("pole.jpg")
    image_width, image_height = image.size
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype("AppleColorEmoji.ttf", 137, index=0)
    text_length = draw.textlength(emoji, font=font)
    text_x = (image_width - text_length) // 2
    text_height = font.getmask(emoji).getbbox()[3]
    text_y = (image_height - text_height) // 2
    draw.text((text_x, text_y), emoji, font=font, embedded_color=True)
    return image

@dp.callback_query_handler(lambda c: c.data == 'krokodil')
async def krokodil(callback_query: types.CallbackQuery):
    message_id = callback_query.message.message_id
    chat_id = callback_query.from_user.id

    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton('🆕 Начать игру', callback_data='start_krokodil'))
    keyboard.add(InlineKeyboardButton('🔙 Назад в меню', callback_data='start'))

    await bot.edit_message_media(
        chat_id=chat_id,
        message_id=message_id,
        media=types.InputMediaPhoto(
        media=open('krokodil.jpg', 'rb'),
        caption="<b>Цель игры - угадать фильм по эмодзи.</b>\n\nНажимай на кнопку ниже, чтобы начать:",
        parse_mode='HTML'),
        reply_markup=keyboard
    )
@dp.callback_query_handler(lambda c: c.data == 'start_krokodil')
async def start_krokodil(callback_query: types.CallbackQuery):
    message_id = callback_query.message.message_id
    user_id = callback_query.from_user.id

    movie = random.choice(list(movies.keys()))
    movie_image = await generate_movie_image(movie)
    image_stream = io.BytesIO()
    movie_image.save(image_stream, format='PNG')
    image_stream.seek(0)
    movie_names = list(movies.keys())
    random_movies = random.sample(list(set(movie_names) - {movie}), min(3, len(movie_names) - 1))
    random_movies.append(movie)
    random.shuffle(random_movies)
    correct_answer = movie

    keyboard = InlineKeyboardMarkup(row_width=2)
    for movie_name in random_movies:
        callback_data = f"{movie_name}:{correct_answer}" if movie_name == movie else f"{movie_name}:"
        keyboard.add(InlineKeyboardButton(movie_name, callback_data=callback_data))
    keyboard.add(InlineKeyboardButton('🔙 Назад в меню', callback_data='start'))

    await bot.edit_message_media(
        chat_id=user_id,
        message_id=message_id,
        media=types.InputMediaPhoto(media=image_stream,
        caption=" ",
        parse_mode='HTML'),
        reply_markup=keyboard
    )
@dp.callback_query_handler(lambda c: ':' in c.data)
async def check_answer(callback_query: types.CallbackQuery):
    message_id = callback_query.message.message_id
    user_id = callback_query.from_user.id
    selected_movie, correct_answer = callback_query.data.split(':')

    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton('🆕 Начать игру', callback_data='start_krokodil'))
    keyboard.add(InlineKeyboardButton('🔙 Назад в меню', callback_data='start'))

    if selected_movie == correct_answer:
        text = '<b>Поздравляю, ты угадал!</b>\n\nЧто делаем дальше?'
        await win(user_id, 'krokodil')
    else:
        text = '<b>Ты не угадал!</b>\n\nЧто делаем дальше?'

    await bot.edit_message_media(
        chat_id=user_id,
        message_id=message_id,
        media=types.InputMediaPhoto(media=open('krokodil.jpg', 'rb'),
        caption=text,
        parse_mode='HTML'),
        reply_markup=keyboard
    )