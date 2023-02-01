from random import randint
from aiogram import types
from global_variable import User
from controller import *
from handlers import *


async def side_win(sides):
    side = 1 if sides == 'Орел' else 0
    win_side = randint(0, 1)
    if side == win_side:
        return True
    return False


async def bot_turn(message: types.Message, users_dict: dict[int, User]):    
    id = message.from_user.id
    player = users_dict[id]
    total = await player.get_total()
    if 28 >= total > 0:
        take = total
    else:
        chance = randint(0, 10)  # Шанс на победу игрока
        if chance % 2 == 0:
            print(f'{await users_dict[id].get_name()} -> это шанс')
            take = randint(1, 28)
        else:
            print(f'{await users_dict[id].get_name()} ->никаких шансов')
            take = total % 29 if total % 29 != 0 else randint(
                1, 28)
    total -= take
    await player.set_total(total)
    print(f'after bot turn {total}. Играем с {await users_dict[id].get_name()}')
    if await check_win(message, users_dict):
        return -1
    return take


async def player_take(message: types.Message, users_dict: dict[int, User]):
    id = message.from_user.id
    player = users_dict[id]
    total = await player.get_total()
    take = int(message.text)
    total -= take
    await player.set_total(total)
    print(f'after {await users_dict[id].get_name()} turn {total}')
    if await check_win(message, users_dict):
        return -1
    return take

async def checking_take(take):
    return True if 0 < take <= 28 else False


async def check_win(message: types.Message, users_dict: dict[int, User]):
    id = message.from_user.id
    player = users_dict[id]
    total = await player.get_total()
    return True if total <= 0 else False
