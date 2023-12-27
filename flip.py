from db import *
@dp.callback_query_handler(lambda c: c.data == 'flip')
async def flip(callback_query: types.CallbackQuery):
    message_id = callback_query.message.message_id
    chat_id = callback_query.from_user.id

    keyboard = InlineKeyboardMarkup()
    keyboard.add(
        InlineKeyboardButton('🦅 Орёл', callback_data='side_head'),
        InlineKeyboardButton('🏵️ Решка', callback_data='side_tail')
    )
    keyboard.add(InlineKeyboardButton('🔙 Назад в меню', callback_data='start'))

    await bot.edit_message_media(
        chat_id=chat_id,
        message_id=message_id,
        media=types.InputMediaPhoto(media=open('flip.jpg', 'rb'),
        caption="<b>Я подброшу монетку, а тебе нужно угадать какая сторона выпадет.</b>\n\nВыбери сторону монетки:",
        parse_mode='HTML'),
        reply_markup=keyboard
    )

@dp.callback_query_handler(lambda c: c.data in ['side_head', 'side_tail'])
async def handle_side_selection(callback_query: types.CallbackQuery):
    message_id = callback_query.message.message_id
    chat_id = callback_query.from_user.id

    selected_side = ' орёл' if callback_query.data == 'side_head' else 'а решка'

    await bot.edit_message_media(
        chat_id=chat_id,
        message_id=message_id,
        media=types.InputMediaPhoto(media=open('flip.jpg', 'rb'),
        caption=f"<b>Джювенс подбрасывает монетку...</b>",
        parse_mode='HTML')
    )

    await asyncio.sleep(3)

    result = random.choice([' орёл', 'а решка'])

    if selected_side == result:
        outcome_text = "Поздравляю, ты угадал сторону!\n\nЧто делаем дальше?"
        await win(chat_id, 'flip')
    else:
        outcome_text = "Ты не угадали сторону.\n\nЧто делаем дальше?"

    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(
        InlineKeyboardButton('🪙 Перебросить монетку', callback_data='flip'),
        InlineKeyboardButton('🔙 Назад в меню', callback_data='start')
    )

    await bot.edit_message_media(
        chat_id=chat_id,
        message_id=message_id,
        media=types.InputMediaPhoto(media=open('flip.jpg', 'rb'),
        caption=f"<b>Выпал{result}.</b>\n\n{outcome_text}",
        parse_mode='HTML'),
        reply_markup=keyboard
    )