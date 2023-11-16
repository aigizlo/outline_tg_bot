import logging
from aiogram import Dispatcher

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from aiogram.utils import executor


from handlers.handlers import get_key_command, my_info
from handlers.send_all import *
from handlers.admin_command import user_info_command
from handlers.handlers_referal_program import process_partners_command
from handlers.handlers_balance import balance_command, replenish_balance_comand, get_amount_for_payment, get_amount_for_payment_2
from text import start_text, promotion_text, not_bot_text
from handlers.handlers_mykeys import *
from handlers.handlers_change_location import *

from aiogram import types
from logger import logger
from user_data import if_new_user
from keyboards.keyboards import capcha
from get_users import sender

User_Data = UserData()


select_key_for_exchange
choosing_new_location
change_location_handlers
get_key_command
process_partners_command
replenish_balance_comand
balance_command
user_info_command
show_rassilka
get_posttext
get_photo
get_photo_id
get_video
get_video_id
get_testpost
sendposts
cancel_post
subscribe
my_info
get_amount_for_payment
get_amount_for_payment_2



scheduler = AsyncIOScheduler()


@dp.message_handler(commands=['start'], state="*")
async def process_start_command(message: types.Message):
    telegram_id = message.from_user.id
    username = message.from_user.first_name
    last_name = message.from_user.last_name
    nickname = message.from_user.username
    language = message.from_user.language_code
    premium = message.from_user.is_premium
    referer_user_id = message.get_args()
    logger.info(f"start command {telegram_id}, {username}, {nickname}")
    try:
        new_user = if_new_user(telegram_id, username, referer_user_id, last_name, nickname, language, premium)
        if not new_user:
            await message.reply(instruction,
                                parse_mode="HTML",
                                disable_web_page_preview=True,
                                reply_markup=main_menu())
            return

        if referer_user_id:
            referer_telegram_id = User_Data.get_tg_if_use_user_id(referer_user_id)
            if referer_telegram_id:
                await bot.send_message(referer_telegram_id, "По вашей ссылке приглашен новый пользователь!")

        await message.reply(not_bot_text,
                            parse_mode="HTML",
                            disable_web_page_preview=True,
                            reply_markup=capcha(),
                            )

        logging.info(f"INFO: NEW USER - tg : {telegram_id}, "
                     f"username : {username}, "
                     f"{referer_user_id}")
        await bot.send_message(chat_id=err_send, text=f"INFO: NEW USER - tg : {telegram_id}, "
                                                      f"username : {username},"
                                                      f"{referer_user_id}")
    except Exception as e:
        await bot.send_message(err_send, f"Ошибка при регистрации нового пользователя ошибка - {e}")
        logging.error(f"ERROR: NEW USER - Ошибка при добавлении нового пользователя "
                      f"tg - {telegram_id}, "
                      f"ошибка - {e}")


@dp.callback_query_handler(lambda c: c.data == "not_bot", state="*")
async def start_to_use_bot(callback_query: types.CallbackQuery):
    telegram_id = callback_query.message.chat.id
    user_id = User_Data.get_user_id(telegram_id)

    # удаляем капчу
    await bot.delete_message(chat_id=callback_query.message.chat.id,
                             message_id=callback_query.message.message_id)
    logger.info(f"Капча пройдена user_id - {user_id}")

    # отправялем пиветственный текст
    await bot.send_message(chat_id=telegram_id, text=start_text,
                        parse_mode="HTML",
                        disable_web_page_preview=True,
                        reply_markup=main_menu())

    # предлагаем пользователю тестовый период
    # await bot.send_message(chat_id=telegram_id,
    #                        text=promotion_text,
    #                        reply_markup=kb_free_tariff,
    #                        parse_mode="HTML",
    #                        )
    logger.info(f'Предложен тестовый период user - {user_id}')


#
def job_function():
    sender()

async def on_startup(dispatcher):
    # Устанавливаем дефолтные команды
    await set_default_commands(dispatcher)
    # Уведомляет про запуск
    await on_startup_notify(dispatcher)


async def on_startup_notify(dp: Dispatcher):
    await dp.bot.send_message(err_send, "Бот Запущен")

if __name__ == '__main__':

    executor.start_polling(dp, on_startup=on_startup, skip_updates=False)
    logger.info('Бот запущен')
