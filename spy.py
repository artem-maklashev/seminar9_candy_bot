from aiogram import types
import datetime

async def log (message: types.Message):
    with open('db.csv', 'a', encoding='utf-8') as file:
        file.write(f'{message.from_user.full_name}, {message.from_user.username},'\
                    f'{datetime.datetime.now().time().replace(microsecond=0)},{message.text}\n')