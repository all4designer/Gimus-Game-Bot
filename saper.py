from db import *

WIDTH = 8
HEIGHT = 8
BOMBS = random.randint(5,10)

field = [[0 for _ in range(WIDTH)] for _ in range(HEIGHT)]
visited = [[False for _ in range(WIDTH)] for _ in range(HEIGHT)]
revealed_cells = set()
bomb_spots = random.sample(range(WIDTH * HEIGHT), BOMBS)
for spot in bomb_spots:
    x, y = spot % WIDTH, spot // WIDTH
    field[y][x] = -1
def check_win():
    total_cells = WIDTH * HEIGHT
    safe_cells_count = total_cells - BOMBS
    revealed_safe_cells = sum(1 for cell in revealed_cells if field[cell[1]][cell[0]] != -1)
    return revealed_safe_cells == safe_cells_count
def count_neighboring_bombs(x, y):
    count = 0
    for i in range(-1, 2):
        for j in range(-1, 2):
            if 0 <= x + i < WIDTH and 0 <= y + j < HEIGHT and field[y + j][x + i] == -1:
                count += 1
    return count
def update_field(x, y):
    if visited[y][x]:
        return
    visited[y][x] = True
    revealed_cells.add((x, y))
    if field[y][x] == 0:
        for i in range(-1, 2):
            for j in range(-1, 2):
                if 0 <= x + i < WIDTH and 0 <= y + j < HEIGHT:
                    update_field(x + i, y + j)

    return
def get_field_keyboard():
    keyboard = types.InlineKeyboardMarkup(row_width=WIDTH)
    for y in range(HEIGHT):
        row = []
        for x in range(WIDTH):
            callback_data = f"cell_{x}_{y}"
            row.append(types.InlineKeyboardButton(text=' ', callback_data=callback_data))
        keyboard.add(*row)
    return keyboard
@dp.callback_query_handler(lambda c: c.data == 'saper')
async def saper(callback_query: types.CallbackQuery):
    message_id = callback_query.message.message_id
    user_id = callback_query.from_user.id

    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton('🆕 Новая игра', callback_data='start_saper'))
    keyboard.add(InlineKeyboardButton('🔙 Назад в меню', callback_data='start'))

    await bot.edit_message_media(chat_id=user_id,
                                 message_id=message_id,
                                 media=types.InputMediaPhoto(media=open('saper.jpg', 'rb'),
                                 caption="<b>Твоя цель - обойти все бомбы.</b>\n\nЦифры ознчают количество мин вокруг этой клетки. Таким образом, нужно раскрыть все поле, избегая их\n\nДля начала игры нажимай кнопку ниже:",
                                 parse_mode='HTML'),
                                 reply_markup=keyboard
    )
@dp.callback_query_handler(lambda c: c.data == 'start_saper')
async def start_saper(callback_query: types.CallbackQuery):
    message_id = callback_query.message.message_id
    user_id = callback_query.from_user.id

    global revealed_cells
    revealed_cells = set()
    for y in range(HEIGHT):
        for x in range(WIDTH):
            field[y][x] = 0
            visited[y][x] = False

    bomb_spots = random.sample(range(WIDTH * HEIGHT), BOMBS)
    for spot in bomb_spots:
        x, y = spot % WIDTH, spot // WIDTH
        field[y][x] = -1

    for y in range(HEIGHT):
        for x in range(WIDTH):
            if field[y][x] != -1:
                field[y][x] = count_neighboring_bombs(x, y)

    keyboard = get_field_keyboard()
    keyboard.add(InlineKeyboardButton('🔙 Назад в меню', callback_data='start'))

    await bot.edit_message_media(chat_id=user_id,
                                 message_id=message_id,
                                 media=types.InputMediaPhoto(media=open('saper.jpg', 'rb'),
                                 caption=" ",
                                 parse_mode='HTML'),
                                 reply_markup=keyboard
    )
def update_empty_cells(x, y):
    if visited[y][x]:
        return
    visited[y][x] = True
    revealed_cells.add((x, y))
    if field[y][x] == 0:
        for i in range(-1, 2):
            for j in range(-1, 2):
                if 0 <= x + i < WIDTH and 0 <= y + j < HEIGHT:
                    update_empty_cells(x + i, y + j)
@dp.callback_query_handler(lambda query: query.data.startswith('cell_'))
async def cell_clicked(callback_query: types.CallbackQuery):
    message_id = callback_query.message.message_id
    chat_id = callback_query.from_user.id

    global revealed_cells
    coordinates = callback_query.data.split('_')
    x, y = int(coordinates[1]), int(coordinates[2])

    if (x, y) in revealed_cells:
        return

    revealed_cells.add((x, y))

    if field[y][x] == -1:
        revealed_cells.remove((x, y))
        for i in range(HEIGHT):
            for j in range(WIDTH):
                revealed_cells.add((j, i))
        keyboard = get_updated_keyboard(0)
        keyboard.add(InlineKeyboardButton('🆕 Новая игра', callback_data='start_saper'))
        keyboard.add(InlineKeyboardButton('🔙 Назад в меню', callback_data='start'))

        await bot.edit_message_media(chat_id=chat_id,
                                     message_id=message_id,
                                     media=types.InputMediaPhoto(media=open('saper.jpg', 'rb'),
                                     caption="<b>Ты проиграл!</b>\n\nЧто делаем дальше?",
                                     parse_mode='HTML'),
                                     reply_markup=keyboard
        )
        return

    update_empty_cells(x, y)

    updated_keyboard = get_updated_keyboard()
    await callback_query.message.edit_reply_markup(reply_markup=updated_keyboard)

    if check_win():
        await win(chat_id, 'saper')
        status = win

        for i in range(HEIGHT):
            for j in range(WIDTH):
                revealed_cells.add((j, i))
        keyboard = get_updated_keyboard(status)
        keyboard.add(InlineKeyboardButton('🆕 Новая игра', callback_data='start_saper'))
        keyboard.add(InlineKeyboardButton('🔙 Назад в меню', callback_data='start'))

        await bot.edit_message_media(chat_id=chat_id,
                                     message_id=message_id,
                                     media=types.InputMediaPhoto(media=open('saper.jpg', 'rb'),
                                     caption="<b>Ты победил!</b>\n\nЧто делаем дальше?",
                                     parse_mode='HTML'),
                                     reply_markup=keyboard)
def get_updated_keyboard(status = None):
    keyboard = types.InlineKeyboardMarkup(row_width=WIDTH)
    for i in range(HEIGHT):
        row = []
        for j in range(WIDTH):
            callback_data = f"cell_{j}_{i}"
            if (j, i) in revealed_cells:
                if field[i][j] == -1:
                    text = '💣'
                elif field[i][j] == 0:
                    text = '◼️'
                else:
                    text = str(field[i][j])
            else:
                text = ' '
            row.append(types.InlineKeyboardButton(text=text, callback_data=callback_data))
        keyboard.add(*row)
    if status == None:
        keyboard.add(InlineKeyboardButton('🔙 Назад в меню', callback_data='start'))

    return keyboard

