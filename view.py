from aiogram import types
import controller
from keyboards import get_keyboard
import handlers

async def rules(message: types.Message):
    await message.answer('По умолчанию установлено количество конфет равное 150, можно изменить введя команду "/set 100", где 100 устанавливаемое значение.')
    await message.answer(f'На столе лежат конфеты. Игроки ходят по очереди.'
                         f'За один ход разрешается брать от 1 до 28 конфет. Кто забрал последние'
                         f'конфеты со стола, тот забирает все конфеты.\n{message.from_user.first_name}, бросим жребий.')


async def bot_play_massage(message: types.Message, take):
    # global candies
    await message.answer(f'Я забрал {take} конфет. Осталось {controller.total}\nТеперь твой ход:')


async def player_message(message: types.Message, take):
    # global candies
    await message.answer(f'Со стола забрали {take} конфет. Осталось {controller.total}')

async def turn_message(message: types.Message, side, win_side: bool):
    if win_side:
        result_side = side
    else:
        result_side = 'Орел' if side == 'Решка' else 'Решка'
    await message.answer(f'Выпал(а) {result_side}\nНа столе {controller.total} конфет')
    if win_side:
        await message.answer(f'{message.from_user.first_name} твой ход')


async def take_error(message: types.Message):
    await message.answer(f'{message.text}!!! Число должно быть больше 0 и меньше 29')


async def player_win(message: types.Message):
    print('победил игрок')
    await handlers.GameStates.coin_choice.set()    
    await message.answer(f'Победитель - {message.from_user.first_name}', reply_markup=get_keyboard())
    

async def bot_win(message: types.Message):
    await handlers.GameStates.coin_choice.set()
    await message.answer(f'Я забрал оставшиеся конфеты и выиграл', reply_markup=get_keyboard())

    