from games import *
from db import *

@dp.message_handler(commands=['start'])
async def start_game(message: types.Message):
    user_id = message.chat.id

    await new_user(user_id)

    keyboard = types.InlineKeyboardMarkup(row_width=2)
    buttons = [
        types.InlineKeyboardButton("🧿 Крестики-нолики", callback_data="tictactoe"),
        types.InlineKeyboardButton("✂️ Камень, ножницы, бумага", callback_data="kmn"),
        types.InlineKeyboardButton("🎰️ Слоты", callback_data="sloti"),
        types.InlineKeyboardButton("🐊 Крокодил", callback_data="krokodil"),
        types.InlineKeyboardButton("🏃‍ Правда или действие", callback_data="pravda"),
        types.InlineKeyboardButton("🪙‍ Орёл и решка", callback_data="flip"),
        types.InlineKeyboardButton("💣 Сапер", callback_data="saper"),
        types.InlineKeyboardButton("🧑‍💻 Мегатест", callback_data="megatest"),
        types.InlineKeyboardButton("📊 Статистика", callback_data="stat")
    ]
    keyboard.add(*buttons)

    await bot.send_photo(
        chat_id=user_id,
        photo=open('menu.jpg', 'rb'),
        caption='<b>Меню</b>\n\nВыберите мини-игру:',
        parse_mode='HTML',
        reply_markup=keyboard
    )

@dp.callback_query_handler(lambda c: c.data == 'start')
async def start_callback(callback_query: types.CallbackQuery):
    message_id = callback_query.message.message_id
    user_id = callback_query.from_user.id

    keyboard = types.InlineKeyboardMarkup(row_width=2)
    buttons = [
        types.InlineKeyboardButton("🧿 Крестики-нолики", callback_data="tictactoe"),
        types.InlineKeyboardButton("✂️ Камень, ножницы, бумага", callback_data="kmn"),
        types.InlineKeyboardButton("🎰️ Слоты", callback_data="sloti"),
        types.InlineKeyboardButton("🐊 Крокодил", callback_data="krokodil"),
        types.InlineKeyboardButton("🏃‍ Правда или действие", callback_data="pravda"),
        types.InlineKeyboardButton("🪙‍ Орёл и решка", callback_data="flip"),
        types.InlineKeyboardButton("💣 Сапер", callback_data="saper"),
        types.InlineKeyboardButton("🧑‍💻 Мегатест", callback_data="megatest"),
        types.InlineKeyboardButton("📊 Статистика", callback_data="stat")
    ]
    keyboard.add(*buttons)

    await bot.edit_message_media(chat_id=user_id,
                                 message_id=message_id,
                                 media=types.InputMediaPhoto(media=open('menu.jpg', 'rb'),
                                 caption="<b>Меню</b>\n\nВыберете мини-игру:",
                                 parse_mode='HTML'),
                                 reply_markup=keyboard
    )

@dp.callback_query_handler(lambda c: c.data == 'stat')
async def stat(callback_query: types.CallbackQuery):
    message_id = callback_query.message.message_id
    user_id = callback_query.from_user.id

    xo_wins, sloti_wins, rocks_wins, pravda_wins, krokodil_wins, megatest_wins, flip_wins, saper_wins = await get_wins(user_id)

    stats_message = (
        f"<b>Статистика по всем играм</b>\n\n"
        f"Крестики-нолики: {xo_wins} побед\n"
        f"Слоты: {sloti_wins} побед\n"
        f"Камень, ножницы, бумага: {rocks_wins} побед\n"
        f"Правда или действие: {pravda_wins} побед\n"
        f"Крокодил: {krokodil_wins} побед\n"
        f"Мегатест: {megatest_wins} побед\n"
        f"Орёл и решка: {flip_wins} побед\n"
        f"Сапер: {saper_wins} побед"
    )

    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton('🔙 Назад в меню', callback_data='start'))

    await bot.edit_message_media(
        chat_id=user_id,
        message_id=message_id,
        media=types.InputMediaPhoto(media=open('stat.jpg', 'rb'),
        caption=stats_message,
        parse_mode='HTML'),
        reply_markup=keyboard
    )

async def restart_bot():
    os.execl(sys.executable, sys.executable, *sys.argv)

@dp.message_handler(commands=['restart'])
async def restart_command(message: types.Message):
    await message.reply("Перезапуск")
    print('Перезапуск')
    await restart_bot()

@dp.message_handler(content_types=['text'])
async def echo(message: types.Message):
    await message.reply("Я бот и не понимаю человеческий, напиши команду /start")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)