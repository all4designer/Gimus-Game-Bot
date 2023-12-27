from db import *

def generate_emoji():
    emojis = ["🍒", "🍇", "💎", "🍋", "7️⃣", "🍉", "🍓", "👑", "🍍"]
    return random.choice(emojis)

@dp.callback_query_handler(lambda c: c.data == 'sloti')
async def sloti(callback_query: types.CallbackQuery):
    message_id = callback_query.message.message_id
    user_id = callback_query.from_user.id

    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton(text="🔄 Вращать автомат", callback_data="start_sloti"))
    keyboard.add(InlineKeyboardButton(text="🔙 Назад в меню", callback_data="start"))


    await bot.edit_message_media(chat_id=user_id,
                                 message_id=message_id,
                                 media=types.InputMediaPhoto(media=open('sloti.jpg', 'rb'),
                                 caption="<b>Цель игры - получить три одинаковых предмета в окне автомата.</b>\n\nНажимай кнопку ниже для старта:",
                                 parse_mode='HTML'),
                                 reply_markup=keyboard
    )
@dp.callback_query_handler(lambda c: c.data == 'start_sloti')
async def start_sloti(callback_query: types.CallbackQuery):
    message_id = callback_query.message.message_id
    user_id = callback_query.from_user.id

    emojis = [generate_emoji() for _ in range(3)]
    emoji_buttons = [InlineKeyboardButton(text=' ', callback_data='empty') for _ in range(3)]

    keyboard = InlineKeyboardMarkup(row_width=3)
    keyboard.add(*emoji_buttons)

    await bot.edit_message_media(chat_id=user_id,
                                 message_id=message_id,
                                 media=types.InputMediaPhoto(media=open('sloti.jpg', 'rb'),
                                 caption="<b>Автомат вращается...</b>",
                                 parse_mode='HTML'),
                                 reply_markup=keyboard
    )

    for i in range(3):
        await asyncio.sleep(1)
        emojis[i] = generate_emoji()
        emoji_buttons[i] = InlineKeyboardButton(text=emojis[i], callback_data='slot_result')

        keyboard = InlineKeyboardMarkup(row_width=3)
        keyboard.add(*emoji_buttons)

        await bot.edit_message_media(chat_id=user_id,
                                     message_id=message_id,
                                     media=types.InputMediaPhoto(media=open('sloti.jpg', 'rb'),
                                     caption="<b>Автомат вращается...</b>",
                                     parse_mode='HTML'),
                                     reply_markup=keyboard
        )

    text = '<b>Не повезло...</b>\n\nПопробуй еще раз!'

    if emojis[0] == emojis[1] == emojis[2]:
        text='<b>Ура, это победа! Поздравляем!</b>\n\nТы можешь попробовать испытать удачу еще раз!'
        await win(user_id, 'sloti')

    keyboard = InlineKeyboardMarkup(row_width=3)
    emoji_buttons = [InlineKeyboardButton(text=emoji, callback_data='slot_result') for emoji in emojis]

    keyboard.add(*emoji_buttons[:3])

    for emoji_button in emoji_buttons[3:]:
        keyboard.add(emoji_button)

    keyboard.add(InlineKeyboardButton(text="🔄 Перекрутить", callback_data="start_sloti"))
    keyboard.add(InlineKeyboardButton(text="🔙 Назад в меню", callback_data="start"))

    await bot.edit_message_media(chat_id=callback_query.message.chat.id,
                                 message_id=callback_query.message.message_id,
                                 media=types.InputMediaPhoto(media=open('sloti.jpg', 'rb'),
                                 caption=f"{text}",
                                 parse_mode='HTML'),
                                 reply_markup=keyboard
    )