import telebot
from telebot import types

import config

token = config.token

sync_bot = telebot.TeleBot(token)

def free_tariff_telebot_kb():
    keyboard = types.InlineKeyboardMarkup(row_width=1)

    a = types.InlineKeyboardButton(text="🎁Попробовать бесплатно", callback_data=f"free_tariff")
    b = types.InlineKeyboardButton(text="Нет, спасибо", callback_data=f"subscribe_no_thanks")
    keyboard.add(a, b)
    return keyboard


def generate_prolong_button(key_name):
    key_name = [(key_name,)]

    keyboard = types.InlineKeyboardMarkup(row_width=1)

    prlg_key = types.InlineKeyboardButton(text=f"👉 Продлить ключ «{key_name[0][0]}» 👈",
                                      callback_data=f"select_key:{key_name[0][0]}")

    cancel = types.InlineKeyboardButton(text="Отмена", callback_data="go_back")

    keyboard.add(prlg_key, cancel)

    return keyboard


def sync_send_message(chat_id, text, parse_mode=None, keyboard=None):
    sync_bot.send_message(chat_id, text, parse_mode=parse_mode, reply_markup=keyboard, disable_web_page_preview=True)


