from aiogram import types
from config import server_id_country
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from config import one_month, two_month, three_month, six_month

def capcha():
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(
        types.InlineKeyboardButton("Я не робот", callback_data="not_bot"),
    )
    return keyboard

def inline_main_menu():
    keyboard = types.InlineKeyboardMarkup(row_width=3)
    keyboard.add(
        types.InlineKeyboardButton("Акции", callback_data="not_bot"),
        types.InlineKeyboardButton("Почему мы?", callback_data="not_bot"),
        types.InlineKeyboardButton("Новостной канал", callback_data="not_bot"),
    )
    return keyboard


def plus_balance():
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(
        types.InlineKeyboardButton("Пополнить баланс")
    )
    return keyboard


def kb_inline_prices():
    keyboard = types.InlineKeyboardMarkup(row_width=4)
    keyboard.add(
        types.InlineKeyboardButton("149", callback_data=f"pr:{149}"),
        types.InlineKeyboardButton("269", callback_data=f"pr:{269}"),
        types.InlineKeyboardButton("380", callback_data=f"pr:{380}"),
        types.InlineKeyboardButton("630", callback_data=f"pr:{630}"),

    )
    return keyboard




# генерация кнопок для продления
def generate_key_buttons(name_keys):
    keyboard = InlineKeyboardMarkup(row_width=1)
    for name in name_keys:
        keyboard.add(InlineKeyboardButton(text=f"«{name[0]}»", callback_data=f"select_key:{name[0]}"))

    keyboard.add(InlineKeyboardButton(text="Отмена", callback_data="go_back"))

    return keyboard

# генерируем имена ключе для выбора одного из них для смены локации
def generate_key_buttons_for_exchange(name_keys):
    keyboard = InlineKeyboardMarkup(row_width=1)
    for name in name_keys:
        keyboard.add(InlineKeyboardButton(text=f"«{name[0]}»", callback_data=f"selecting_key_for_exchange:{name[0]}"))

    keyboard.add(InlineKeyboardButton(text="Отмена", callback_data="go_back"))

    return keyboard

# генерим имена серверов
def generate_location_button(servers):
    keyboard = InlineKeyboardMarkup(row_width=1)
    for server in servers:
        location = server_id_country.get(server)
        keyboard.add(InlineKeyboardButton(text=location, callback_data=f"select_country_for_exchange:{server}"))
    keyboard.add(InlineKeyboardButton(text="Отмена", callback_data="go_back"))

    return keyboard


# кнопка для создания промокода
def subscribe():
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(
        types.InlineKeyboardButton("Подписаться на канал", url="https://t.me/off_radar"),
        types.InlineKeyboardButton("Я уже подписан", callback_data="subscribe_ago"),
        types.InlineKeyboardButton("Нет, спасибо", callback_data="subscribe_no_thanks"),

    )
    return keyboard


# Cпособы оплаты
def get_pay_method_keyboard():
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(
        types.InlineKeyboardButton("💰Cписать с баланса Личного кабинета", callback_data=f"balance_pay_sever"),
        types.InlineKeyboardButton("Отмена", callback_data="go_back")
    )
    return keyboard


def kb_pay(amount, any_pay_link, fk_link=None):
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(
        types.InlineKeyboardButton(f"Карта / СПБ - {amount} рублей", url=any_pay_link),
        types.InlineKeyboardButton(f"Карта / СПБ / Моб.Платеж / USDT - {amount} рублей", url=fk_link),
        types.InlineKeyboardButton("Отмена", callback_data="go_back")
    )
    return keyboard

#
# def free_tariff():
#     keyboard = types.InlineKeyboardMarkup(row_width=1)
#     keyboard.add(
#         types.InlineKeyboardButton("🎁Попробовать бесплатно", callback_data=f"subscribe_ago"),
#         types.InlineKeyboardButton("Нет, спасибо", callback_data=f"subscribe_no_thanks"),
#     )
#     return keyboard




# кнопка для создания промокода
def promocode():
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(
        types.InlineKeyboardButton("Создать промокод", callback_data=f'promo_code'),
        types.InlineKeyboardButton("Отмена", callback_data="go_back")
    )
    return keyboard


# кнопка Баланс
def balance_keyboard():
    keyboard = types.ReplyKeyboardMarkup(row_width=2)
    button_balance = types.KeyboardButton('Пополнить баланс')
    button = types.KeyboardButton('🔙Назад'
                                  '')
    keyboard.add(button_balance, button)

    return keyboard


# кнопка Назад
def main_menu():
    keyboard = types.ReplyKeyboardMarkup(row_width=2)
    button1 = types.KeyboardButton('🔐Получить ключ')
    button2 = types.KeyboardButton('🔑Мои ключи')
    button3 = types.KeyboardButton('💰Баланс')
    button4 = types.KeyboardButton('💵Партнерская программа')
    # button5 = types.KeyboardButton('Инструкция')
    keyboard.add(button1, button2, button3, button4)

    return keyboard

# для выбора месяца, на который будет продлеваться ключ
def choice_renewal_period():
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(
        types.InlineKeyboardButton(f"1 месяц – {one_month} рублей", callback_data=f'renewal:{1}'),
        types.InlineKeyboardButton(f"2 месяца – {two_month} рублей Скидка 10%", callback_data=f"renewal:{2}"),
        types.InlineKeyboardButton(f"3 месяца – {three_month} рублей Скидка 15%", callback_data=f"renewal:{3}"),
        types.InlineKeyboardButton("Отмена", callback_data="go_back")
    )
    return keyboard


# Получить ключ
def choice_period():
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(
        types.InlineKeyboardButton(f"🎁 Бесплатно для новых пользователей 🎁", callback_data=f'subscribe_ago'),
        types.InlineKeyboardButton(f"1 месяц – {one_month} рублей", callback_data=f'get_keys:{1}'),
        types.InlineKeyboardButton(f"2 месяца – {two_month} рублей Скидка 10%", callback_data=f"get_keys:{2}"),
        types.InlineKeyboardButton(f"3 месяца – {three_month} рублей Скидка 15%", callback_data=f"get_keys:{3}"),
        types.InlineKeyboardButton("Отмена", callback_data="go_back")
    )
    return keyboard
# Получить ключ без бесплатного
def choice_period_not_free():
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(
        types.InlineKeyboardButton(f"1 месяц – {one_month} рублей", callback_data=f'get_keys:{1}'),
        types.InlineKeyboardButton(f"2 месяца – {two_month} рублей Скидка 10%", callback_data=f"get_keys:{2}"),
        types.InlineKeyboardButton(f"3 месяца – {three_month} рублей Скидка 15%", callback_data=f"get_keys:{3}"),
        types.InlineKeyboardButton("Отмена", callback_data="go_back")
    )
    return keyboard

def subscribe():
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(
        types.InlineKeyboardButton("Подписаться на канал", url="https://t.me/off_radar"),
        types.InlineKeyboardButton("Я уже подписан", callback_data="subscribe_ago")
    )
    return keyboard


def back_button():
    keyboard = types.ReplyKeyboardMarkup(row_width=1)
    button = types.KeyboardButton('🔙Назад')
    keyboard.add(button)

    return keyboard


def back_and_buy_button():
    keyboard = types.ReplyKeyboardMarkup(row_width=1)
    buy_button = types.KeyboardButton('🔐Получить ключ')
    button_back = types.KeyboardButton('🔙Назад')
    keyboard.add(buy_button, button_back)

    return keyboard


def back_and_prolong_button():
    keyboard = types.ReplyKeyboardMarkup(row_width=1)

    button_back = types.KeyboardButton('🔙Назад')

    prolong_button = types.KeyboardButton('⌛️Продлить действие ключей')

    exchange_key = types.KeyboardButton('🔁Сменить локацию VPN')

    buy_button = types.KeyboardButton('🔐Получить еще ключ')

    keyboard.add(exchange_key, prolong_button, buy_button, button_back)

    return keyboard


def back_and_withdraw():
    keyboard = types.ReplyKeyboardMarkup(row_width=1)

    button_back = types.KeyboardButton('🔙Назад')

    withdraw = types.KeyboardButton('Вывод средств')

    keyboard.add(withdraw, button_back)

    return keyboard
