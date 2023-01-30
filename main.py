from aiogram import types
from aiogram import executor
from handlers import dp

async def on_start(_):
    print('Бот запущен')
    await set_default_commands(dp)

async def set_default_commands(dp):
    await dp.bot.set_my_commands([
        types.BotCommand("start", "Запустить бота"),
        types.BotCommand("cancel", "Отмена"),
        # types.BotCommand("set", "Установить количество конфет после начала игры"),
        # types.BotCommand("form", "Форма"),
        # types.BotCommand("menu", "Меню"),
    ])

executor.start_polling(dp, skip_updates=True, on_startup=on_start)