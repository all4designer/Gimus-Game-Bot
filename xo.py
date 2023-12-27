from db import *

games = {}
def check_draw(game_map):
    for row in game_map:
        if " " in row:
            return False
    return True

async def send_game_message(user_id, message_id, game_data):
    skip = False

    x_emoji = "❌"
    o_emoji = "⭕️"

    for row in game_data['game_map']:
        row_display = ""
        for cell in row:
            if cell == "X":
                row_display += x_emoji
            elif cell == "O":
                row_display += o_emoji
            else:
                row_display += " "
            row_display += " "

    if check_win("❌", game_data['game_map']):
        text = "<b>Ты победил!</b>\n\nЧто делаем дальше?"
        game_data['game_over'] = True
        await win(user_id, 'xo')

    elif check_win("⭕️", game_data['game_map']):
        text = "<b>Я победил!</b>\n\nЧто делаем дальше?"
        game_data['game_over'] = True
    elif check_draw(game_data['game_map']):
        text = "<b>Ничья!</b>\n\nЧто делаем дальше?"
        game_data['game_over'] = True

    elif game_data['current_player'] == "❌":
        text = "<b>Твой ход.</b>\n\nКуда походишь?"
    else:
        text = "<b>Думаю куда-бы походить...</b>"
        skip = True

    # тут генератор кнопок вынести, если надо чтобы пользователь видел процесс хода / иначе можно бота поломать пизец полный
    keyboard = types.InlineKeyboardMarkup()
    if skip == False:
        for i in range(3):
            buttons_row = [
                types.InlineKeyboardButton(
                    text=game_data['game_map'][i][j] if game_data['game_map'][i][j] != " " else " ",
                    callback_data=f"move_{i}_{j}"
                ) for j in range(3)
            ]
            keyboard.row(*buttons_row)
        if game_data['game_over'] == True:
            keyboard.add(InlineKeyboardButton('🆕 Новая игра', callback_data='start_tictactoe'))
        keyboard.add(InlineKeyboardButton(text="🔙 Назад в меню", callback_data="start"))


    await bot.edit_message_media(chat_id=user_id,
                                 message_id=message_id,
                                 media=types.InputMediaPhoto(media=open('xo.jpg', 'rb'),
                                 caption=f"{text}",
                                 parse_mode='HTML'),
                                 reply_markup=keyboard)

def initialize_game(message_id):
    games[message_id] = {
        'game_map': [
            [" ", " ", " "],
            [" ", " ", " "],
            [" ", " ", " "]
        ],
        'current_player': "❌",
        'game_over': False
    }

def bot_move(game_data):
    empty_cells = [(i, j) for i in range(3) for j in range(3) if game_data['game_map'][i][j] == " "]
    if empty_cells:
        row, col = random.choice(empty_cells)
        game_data['game_map'][row][col] = game_data['current_player']
        game_data['current_player'] = "❌" if game_data['current_player'] == "⭕️" else "⭕️"
@dp.callback_query_handler(lambda c: c.data == 'tictactoe')
async def tictactoe(callback_query: types.CallbackQuery):
    chat_id = callback_query.message.chat.id
    message_id = callback_query.message.message_id

    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton('🆕 Новая игра', callback_data='start_tictactoe'))
    keyboard.add(InlineKeyboardButton('🔙 Назад в меню', callback_data='start'))

    await bot.edit_message_media(
        chat_id=chat_id,
        message_id=message_id,
        media=types.InputMediaPhoto(media=open('xo.jpg', 'rb'),
        caption="<b>Побеждает тот, у кого будет 3 в ряд одинаковых символа.</b>\n\nВсе абсолютно честно, я случайно решу кто первый будет ходить.\n\nНачинай новую игру:",
        parse_mode='HTML'),
        reply_markup=keyboard
    )
@dp.callback_query_handler(lambda c: c.data == 'start_tictactoe')
async def start_tictactoe(callback_query: types.CallbackQuery):
    chat_id = callback_query.message.chat.id
    message_id = callback_query.message.message_id

    await bot.edit_message_media(
        chat_id=chat_id,
        message_id=message_id,
        media=types.InputMediaPhoto(media=open('xo.jpg', 'rb'),
        caption="<b>Случайным образом выбираю кто будет первый ходить...</b>",
        parse_mode='HTML'),
    )

    await asyncio.sleep(3)

    initialize_game(message_id)
    games[message_id]['current_player'] = random.choice(["❌", "⭕️"])

    if games[message_id]['current_player'] == "⭕️":
        text = '<b>Я первый!</b>\n\nУже думаю куда похожу...'
        bot_move(games[message_id])
    else:
        text = '<b>Ты первый!</b>\n\nЯ уже подготавливаю поле...'
    await bot.edit_message_media(
        chat_id=chat_id,
        message_id=message_id,
        media=types.InputMediaPhoto(media=open('xo.jpg', 'rb'),
        caption=text,
        parse_mode='HTML'),
    )

    await asyncio.sleep(2)

    await send_game_message(chat_id, message_id, games[message_id])
@dp.callback_query_handler(lambda c: c.data.startswith('move_'))
async def process_move(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    message_id = callback_query.message.message_id

    _, row, col = callback_query.data.split('_')
    row, col = int(row), int(col)

    if message_id in games:
        game_data = games[message_id]

        if not game_data['game_over'] and game_data['game_map'][row][col] == " ":
            game_data['game_map'][row][col] = game_data['current_player']

            if check_win("❌", game_data['game_map']) or check_win("⭕️", game_data['game_map']) or check_draw(game_data['game_map']):
                await send_game_message(user_id, message_id, game_data)
            else:
                game_data['current_player'] = "⭕️" if game_data['current_player'] == "❌" else "❌"
                await send_game_message(user_id, message_id, game_data)

                if not game_data['game_over']:
                    await asyncio.sleep(3)
                    bot_move(game_data)
                    await send_game_message(user_id, message_id, game_data)
def check_win(player, game_map):
    for i in range(3):
        if game_map[i][0] == game_map[i][1] == game_map[i][2] == player:
            return True
        if game_map[0][i] == game_map[1][i] == game_map[2][i] == player:
            return True
    if game_map[0][0] == game_map[1][1] == game_map[2][2] == player:
        return True
    if game_map[0][2] == game_map[1][1] == game_map[2][0] == player:
        return True
    return False