from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from tokens import bot_token
from logic import get_map_cell, check_step
from keyboards import kb_player

async def on_startup(_):
    print('Бот вышел в онлайн!')

bot = Bot(bot_token())
dp = Dispatcher(bot)

cols, rows = 4,4

maps = {}

def map_to_str(map_cell, player) -> str:
    map_str = ""
    for y in range(rows * 2 - 1):
        for x in range(cols * 2 - 1):
            if map_cell[x + y * (cols * 2 - 1)]:
                map_str += "\U00002B1B"
            elif (x, y) == player:
                map_str += "\U0001F534"
            else:
                map_str += "\U00002B1C"
        map_str += '\n'
    return map_str


@dp.message_handler(commands=['play'])
async def play_message(message: types.Message):
    map_cell = get_map_cell(cols, rows)

    user_data = {
        'map': map_cell,
        'x': 0,
        'y': 0
    }

    maps[message.chat.id] = user_data

    await message.answer(map_to_str(map_cell, (0, 0)), reply_markup=kb_player)


@dp.callback_query_handler(lambda x: True)
async def callback_query(c_message: types.CallbackQuery):
    user_data = maps[c_message.message.chat.id]
    res = check_step(user_data, c_message.data)
    if len(res) > 0:
        user_data['x'], user_data['y'] = res

        await bot.edit_message_text(chat_id=c_message.message.chat.id,
                                    message_id=c_message.message.message_id,
                                    text=map_to_str(user_data['map'], (user_data['x'], user_data['y'])),
                                    reply_markup=kb_player)
    await c_message.answer()

executor.start_polling(dp, skip_updates=True, on_startup=on_startup)






















