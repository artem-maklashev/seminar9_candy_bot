from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

def get_keyboard():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(KeyboardButton('Начать игру'))
    return kb


def get_cancel():
    return ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton('/cancel'))


def get_coin_side():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ['Орел', 'Решка']
    kb.add(*buttons)
    return kb
