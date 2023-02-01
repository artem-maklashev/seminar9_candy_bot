# from controller import side_win
from create import dp
from keyboards import *
# from view import rules
# import controller
from controller import lets_play, player_turn
from spy import *
from aiogram import types
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext
from global_variable import User, candies

class GameStates(StatesGroup):
    coin_choice = State()
    game_process = State()

users_dict = {}

async def rules(message: types.Message):
    await message.answer('По умолчанию установлено количество конфет равное 150, можно изменить введя команду "/set 100", где 100 устанавливаемое значение.')
    await message.answer(f'На столе лежат конфеты. Игроки ходят по очереди.'
                         f'За один ход разрешается брать от 1 до 28 конфет. Кто забрал последние'
                         f'конфеты со стола, тот забирает все конфеты.\n{message.from_user.first_name}, бросим жребий.')


async def player_win(message: types.Message):
    print('победил игрок')
    await GameStates.coin_choice.set()
    await message.answer(f'Победитель - {message.from_user.first_name}', reply_markup=get_keyboard())


async def bot_win(message: types.Message):
    await GameStates.coin_choice.set()
    await message.answer(f'Я забрал оставшиеся конфеты и выиграл', reply_markup=get_keyboard())



@dp.message_handler(commands=['start'], state=None)
async def game_command(message: types.Message):
    global player
    
    id = message.from_user.id   
       
    
    await log(message)
    await message.answer('Нажми ↓ "Начать игру" ↓ ', reply_markup=get_keyboard())


@dp.message_handler(commands=['set'], state=GameStates.coin_choice)
async def game_command(message: types.Message):
    await log(message)
    global player
    id = message.from_user.id
    total = int(message.text.split()[1])
    await player.set_total(total) 
    global users_dict
    users_dict[id] = player   
    await message.answer(f'Установлено количество конфет {total}', reply_markup=get_keyboard())

@dp.message_handler(Text(equals='Начать игру', ignore_case=True), state='*')
async def start_game(message: types.Message):
    await log(message)
    await GameStates.coin_choice.set()
    await rules(message)
    await message.answer('Выбери орел или решка', reply_markup=get_coin_side())


@dp.message_handler(Text(equals=['Орел', 'Решка']), state=GameStates.coin_choice)
async def coin_side(message: types.Message):
    id = message.from_user.id
    name = message.from_user.full_name
    global player
    player = User(name, candies)
    global users_dict
    users_dict[id] = player
    await log(message)
    await GameStates.game_process.set()
    side = message.text
    await message.answer(f'Вы выбрали {side}', reply_markup=get_cancel())
    await lets_play(message, users_dict)

@dp.message_handler(state=GameStates.game_process)
async def processing(message: types.Message, state: FSMContext):
    await log(message)
    if message.text.isnumeric():
        await player_turn(message, users_dict)
    elif message.text == '/cancel':
        await state.finish()
        await message.answer('Игра окончена', reply_markup=get_keyboard())


@dp.message_handler(commands=['cancel'], state='*')
async def game_command(message: types.Message, state: FSMContext):
    await log(message)
    current_state = await state.get_state()
    if current_state is None:
        await message.answer('Основное меню', reply_markup=types.ReplyKeyboardRemove())
        return
    await state.finish()
    await message.answer('Основное меню', reply_markup=get_keyboard())
    
  
