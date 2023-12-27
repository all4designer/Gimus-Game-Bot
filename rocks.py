from db import *
@dp.callback_query_handler(lambda c: c.data == 'kmn')
async def kmn(callback_query: types.CallbackQuery):
    message_id = callback_query.message.message_id
    user_id = callback_query.from_user.id

    keyboard = types.InlineKeyboardMarkup()
    buttons = [
        types.InlineKeyboardButton(text="🗿 Камень", callback_data="rock"),
        types.InlineKeyboardButton(text="✂️ Ножницы", callback_data="scissors"),
        types.InlineKeyboardButton(text="📃 Бумага", callback_data="paper"),
        types.InlineKeyboardButton(text="🔙 Назад в меню", callback_data="start")
    ]
    keyboard.add(*buttons)

    await bot.edit_message_media(chat_id=user_id,
                                 message_id=message_id,
                                 media=types.InputMediaPhoto(media=open('kmn.jpg', 'rb'),
                                 caption="<b>Классическая игра, классические правила.</b>\n\nВыбери свой ход:",
                                 parse_mode='HTML'),
                                 reply_markup=keyboard
    )
@dp.callback_query_handler(lambda c: c.data in ["rock", "scissors", "paper"])
async def kmn_start(callback_query: types.CallbackQuery):
    user_choice = callback_query.data
    message_id = callback_query.message.message_id
    user_id = callback_query.from_user.id

    await bot.edit_message_media(chat_id=user_id,
                                 message_id=message_id,
                                 media=types.InputMediaPhoto(media=open('kmn.jpg', 'rb'),
                                 caption=f"<b>Теперь я думаю что выбрать...</b>",
                                 parse_mode='HTML')
    )

    await asyncio.sleep(2)

    bot_choice = random.choice(["rock", "scissors", "paper"])

    choices = {
        "rock": "камень",
        "scissors": "ножницы️",
        "paper": "бумага"
    }

    if user_choice == bot_choice:
        result_text = f"<b>Ничья!</b>\n\nТвой ход: {choices[user_choice]}\nМой ход: {choices[bot_choice]}"
    elif (user_choice == "rock" and bot_choice == "scissors") or (user_choice == "scissors" and bot_choice == "paper") or (user_choice == "paper" and bot_choice == "rock"):
        await win(user_id, 'kmn')
        result_text = f"<b>Ты победил!</b>\n\nТвой ход: {choices[user_choice]}\nМой ход: {choices[bot_choice]}"
    else:
        result_text = f"<b>Ты проиграл!</b>\n\nТвой ход: {choices[user_choice]}\nМой ход: {choices[bot_choice]}"

    keyboard = types.InlineKeyboardMarkup(row_width=1)
    buttons = [
        types.InlineKeyboardButton(text="🆕 Новая игра", callback_data="kmn"),
        types.InlineKeyboardButton(text="🔙 Назад в меню", callback_data="start")
    ]
    keyboard.add(*buttons)

    await bot.edit_message_media(chat_id=user_id,
                                 message_id=message_id,
                                 media=types.InputMediaPhoto(media=open('kmn.jpg', 'rb'),
                                 caption=f"{result_text}\n\nЧто делаем дальше?",
                                 parse_mode='HTML'),
                                 reply_markup=keyboard
    )