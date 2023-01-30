# from controller import side_win
from create import dp
from keyboards import *
import view
import controller
import spy
from aiogram import types
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext



class GameStates(StatesGroup):
    coin_choice = State()
    game_process = State()


@dp.message_handler(commands=['start'], state=None)
async def game_command(message: types.Message):
    await spy.log(message)
    await message.answer('Нажми ↓ "Начать игру" ↓ ', reply_markup=get_keyboard())


@dp.message_handler(commands=['set'], state=GameStates.coin_choice)
async def game_command(message: types.Message):
    await spy.log(message)
    controller.total = int(message.text.split()[1])
    await message.answer(f'Установлено количество конфет {controller.total}', reply_markup=get_keyboard())

@dp.message_handler(Text(equals='Начать игру', ignore_case=True), state='*')
async def start_game(message: types.Message):
    await spy.log(message)
    await GameStates.coin_choice.set()
    await view.rules(message)
    await message.answer('Выбери орел или решка', reply_markup=get_coin_side())


@dp.message_handler(Text(equals=['Орел', 'Решка']), state=GameStates.coin_choice)
async def coin_side(message: types.Message):
    await spy.log(message)
    await GameStates.game_process.set()
    side = message.text
    await message.answer(f'Вы выбрали {side}', reply_markup=get_cancel())
    await controller.lets_play(message)

@dp.message_handler(state=GameStates.game_process)
async def processing(message: types.Message, state: FSMContext):
    await spy.log(message)
    if message.text.isnumeric():
        await controller.player_turn(message)
    elif message.text == '/cancel':
        await state.finish()
        await message.answer('Игра окончена', reply_markup=get_keyboard())


@dp.message_handler(commands=['cancel'], state='*')
async def game_command(message: types.Message, state: FSMContext):
    await spy.log(message)
    current_state = await state.get_state()
    if current_state is None:
        await message.answer('Основное меню', reply_markup=types.ReplyKeyboardRemove())
        return
    await state.finish()
    await message.answer('Основное меню', reply_markup=get_keyboard())
    current_state = await state.get_state()
    if current_state in GameStates:
        if current_state == 'GameStates:coin_choice':
            print('coin_choice')
        elif current_state == 'GameStates:game_process':
            print('game_process')
        else:
            print('None')
  
