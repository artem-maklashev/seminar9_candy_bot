from aiogram import types



async def bot_play_massage(message: types.Message, take, total):
    
    
    await message.answer(f'Я забрал {take} конфет. Осталось {total}\nТеперь твой ход:')


async def player_message(message: types.Message, take, total):
    # id = get_user_id(message)
    
    await message.answer(f'Со стола забрали {take} конфет. Осталось {total}')

async def turn_message(message: types.Message, side, win_side: bool, total):
    # id = int(message.from_user.id)
    if win_side:
        result_side = side
    else:
        result_side = 'Орел' if side == 'Решка' else 'Решка'
    await message.answer(f'Выпал(а) {result_side}\nНа столе {total} конфет')
    if win_side:
        await message.answer(f'{message.from_user.first_name} твой ход')


async def take_error(message: types.Message):
    await message.answer(f'{message.text}!!! Число должно быть больше 0 и меньше 29')




