from config import *

async def connect():
    conn = sqlite3.connect('game_stats.db')
    cursor = conn.cursor()

    return cursor, conn
async def new_user(user_id):
    cursor, conn = await connect()

    cursor.execute('SELECT * FROM user_stats WHERE user_id = ?', (user_id,))
    user_exists = cursor.fetchone()

    # Если пользователь не найден, добавляем его в базу данных
    if not user_exists:
        cursor.execute('''
            INSERT INTO user_stats (user_id, xo_wins, sloti_wins, kmn_wins, pravda_wins, krokodil_wins, megatest_wins, flip_wins, saper_wins)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (user_id, 0, 0, 0, 0, 0, 0, 0, 0))
        conn.commit()

    conn.close()
async def get_wins(user_id):
    cursor, conn = await connect()

    cursor.execute('SELECT * FROM user_stats WHERE user_id = ?', (user_id,))
    user_stats = cursor.fetchone()

    xo_wins, sloti_wins, rocks_wins, pravda_wins, krokodil_wins, megatest_wins, flip_wins, saper_wins = user_stats[1:]
    conn.close()

    return xo_wins, sloti_wins, rocks_wins, pravda_wins, krokodil_wins, megatest_wins, flip_wins, saper_wins
async def win(user_id, game):
    cursor, conn = await connect()
    with conn:
        cursor.execute(f'''
            UPDATE user_stats 
            SET {game}_wins = {game}_wins + 1 
            WHERE user_id = ?
        ''', (user_id,))
        conn.commit()
    conn.close()
