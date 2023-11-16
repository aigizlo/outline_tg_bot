from aiogram import Dispatcher
from config import err_send

async def on_startup_notify(dp: Dispatcher):
    await dp.bot.send_message(err_send, "Бот Запущен")
