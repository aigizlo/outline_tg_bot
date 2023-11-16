from config import one_month, two_month, three_month, six_month, support

not_bot_text = "Что бы пользоваться телеграм-ботом, пожалуйста, подтвердите, что вы не робот. Нажмите на «Я не робот»"

answer_not_keys = """У вас нет ключей🙁
                
Чтобы приобрести ключ доступа, нажмите "Получить ключ" """

instruction_and_main_menu = """
📌Как пользоваться VPN?
<b>✅Шаг 1:</b> Скачайте приложение <a href="https://play.google.com/store/apps/details?id=org.outline.android.client">Android</a>, <a href="https://apps.apple.com/us/app/outline-app/id1356177741">iPhone</a>, <a href="https://s3.amazonaws.com/outline-releases/client/windows/stable/Outline-Client.exe">Windows</a>, <a href="https://apps.apple.com/us/app/outline-app/id1356178125">MacOS</a>
<b>✅Шаг 2:</b> Скопируйте ваш ключ и вставьте в приложение Outline
<b>✅Шаг 3:</b> Нажмите кнопку «Подключиться»

<b><a href="https://t.me/off_radar">🔔Следите за нашими акциями</a></b>

<b><a href="https://telegra.ph/Kak-rabotaet-servis-Outline-Nadezhnost-i-Ustojchivost-k-Blokirovkam-10-03">💡Почему Off Radar?</a></b>

🏪Служба поддержки работает 24 часа – <a href="https://t.me/off_radar_support">@off_radar_support</a>

Главное меню бота 👇👇👇
"""

instruction = """

📌Как пользоваться VPN?
<b>✅Шаг 1:</b> Скачайте приложение <a href="https://play.google.com/store/apps/details?id=org.outline.android.client">Android</a>, <a href="https://apps.apple.com/us/app/outline-app/id1356177741">iPhone</a>, <a href="https://s3.amazonaws.com/outline-releases/client/windows/stable/Outline-Client.exe">Windows</a>, <a href="https://apps.apple.com/us/app/outline-app/id1356178125">MacOS</a>
<b>✅Шаг 2:</b> Скопируйте ваш ключ и вставьте в приложение Outline
<b>✅Шаг 3:</b> Нажмите кнопку «Подключиться»

<b><a href="https://t.me/off_radar">🔔Следите за нашими акциями</a></b>

<b><a href="https://telegra.ph/Kak-rabotaet-servis-Outline-Nadezhnost-i-Ustojchivost-k-Blokirovkam-10-03">💡Почему Off Radar?</a></b>

🏪Служба поддержки работает 24 часа – <a href="https://t.me/off_radar_support">@off_radar_support</a>
"""

start_text = f"""Привет! Я <b>«Off Radar»!</b>. Подключайся к любым веб-ресурсам <b>безопасно и быстро</b> с помощью своего персонального <b>VPN</b>.

🚀Быстрый VPN <b>без ограничений</b>, ты сможешь наслаждаться <b>Инстаграмом</b>, <b>Facebook'ом</b>,  фильмами в 4K и HD на <b>YouTube</b>.

😎Гарантированная <b>защита от блокировок</b>! Приватный VPN только для вас, он не блокируется в отличие от публичных сервисов.

📲Что бы начать, скачай приложение <b>Outline</b> на свое устройство: <a href="https://play.google.com/store/apps/details?id=org.outline.android.client">Android</a>, <a href="https://apps.apple.com/us/app/outline-app/id1356177741">iPhone</a>, <a href="https://raw.githubusercontent.com/Jigsaw-Code/outline-releases/master/client/stable/Outline-Client.exe">Windows</a>, <a href="https://apps.apple.com/us/app/outline-app/id1356178125">MacOS</a>

🔐И жми <b>«Получить ключ»</b> в главном меню 👇👇👇"""

promotion_text = """🎁Для всех новых пользователей мы предлагаем 3 дня тестового периода!🎁"""


promo_text = f'''Добро пожаловать в партнерскую программу «Off Radar»! 💼🚀

Мы рады пригласить вас стать частью нашего растущего сообщества и получить возможность зарабатывать, делая интернет более доступным и безопасным для ваших друзей. Представляем вам нашу выгодную и простую партнерскую программу на основе промокодов.

🔥 Как это работает?

Создайте свой уникальный промокод в вашем личном кабинете.
Поделитесь промокодом со своими друзьями, коллегами и родственниками.
Когда они используют ваш промокод, они получают 20% скидку на свою покупку.
Вы получаете 20% от стоимости их покупки в виде комиссии на свой счет.
🌟 Преимущества нашей партнерской программы:

Активируя ваш промокод, ваши друзья получают выгодное предложение, которое повышает шансы на их участие.
Вы получаете стимул продвигать наш сервис, получая вознаграждение за каждого привлеченного пользователя.
Разделяя выгоду между вами и вашими друзьями, мы создаем взаимовыгодное сотрудничество и расширяем наше сообщество.
💡 Маркетинговые советы:

Расскажите о преимуществах Off Radar в социальных сетях, форумах и блогах.
Составьте подробный обзор нашего сервиса и опубликуйте его на своем веб-сайте или блоге.
Сделайте видео-обзор с демонстрацией работы Off Radar и поделитесь им в социальных сетях и на YouTube.
Не упустите возможность присоединиться к нашей партнерской программе и начать зарабатывать уже сегодня! Вместе мы сделаем интернет более безопасным и доступным для всех! 💪🌐'''

answer_error = f"Произошла ошибка!\n" \
               f"Пожалуйста, попробуйте снова или обратитесь в службу поддержки {support}"


# Копирующийся промокод
def promocode_text(promocode):
    text = f"""
    Ваш промокод: `{promocode[0]}`

    Приглашайте ваших друзей в Off Radar @off_radar_bot и получайте 20% от их покупок и продления\.

    ‼ВНИМАНИЕ‼
    Ваш промокод действителен только при действующей подписке\!
    """
    return text


def ref_link(user_id, bot_name, count, balance):
    text = f"Добро пожаловать в нашу партнерскую программу!\n\n" \
           f"Приглашай друзей по своей реферальной ссылке и получай 20% от их каждой покупки и продления!!!\n\n" \
           f"Это реальная возможность создать свой пассивный доход!\n\n" \
           f"Ваш ID : {user_id}\n\n" \
           f"Ваша реферальная ссылка : <code>https://t.me/{bot_name}?start={user_id}</code>\n\n" \
           f"Вы пригласили: {count} человек\n\n" \
           f"Ваш баланс партнерский баланс: {balance} рублей"

    return text


def payment_amount_prompt(amount):
    text = f"Сумма покупки {amount} рублей, выберите способ оплаты:"

    return text


subscription_prompt = "Выберите, на сколько месяцев оформить подписку"


# ответы об оплате
def answer_if_buy(key_value, location):
    global instruction
    answer_if_buy = f"""Покупка прошла успешно👌!
    
Спасибо, что выбрали <b>«Off Radar»!!</b> 😇

Ваш ключ:
    – <code>{key_value}</code>
(👆кликни для копирования)

Локация : {location}

Управляйте вашими ключами доступа в разделе «Мои ключи»
"""
    return answer_if_buy + instruction


# ответы об оплате
def answer_if_change(key_value, location):
    global instruction
    answer_if_buy = f"""Смена локации прошла успешно👌!

Ваш ключ:
    – <code>{key_value}</code>
(👆кликни для копирования)

Локация: {location}

Управляйте вашими ключами доступа в разделе «Мои ключи»
"""
    return answer_if_buy + instruction


answer_if_not_balance = "Недостаточно средств. Пожалуйста, пополните ваш баланс.\n" \
                        "👇Выберите необходимую сумму для оплаты👇"

# offer_free_plan = "Для всех новых пользователей, мы предлагаем 14 дней бесплатного пользования😎\nВ обмен на подписку " \
#                   "на наш канал\n👇👇👇Возьми наш подарок👇👇👇 "
#
# offer_free_plan_2 = "Для всех новых пользователей, мы предлагаем 14 дней бесплатного пользования😎\n👇👇👇Возьми наш " \
#                   "подарок👇👇👇 "


def text_free_tariff(key_value):
    txt = f"Спасибо, что выбрали <b>«Off Radar»!!</b> 😇\n" \
          f"Ваш ключ:\n\n" \
          f"– 🔑 <code>{key_value}</code> 🔒\n" \
          f"(👆кликни для копирования)\n\n" \
          f"📲<b>Инструкция:</b>\n\n"\
          f"""<b>✅Шаг 1:</b> Скачайте приложение Outline <a href="https://play.google.com/store/apps/details?id=org.outline.android.client">Android</a>, <a href="https://apps.apple.com/us/app/outline-app/id1356177741">iPhone</a>, <a href="https://s3.amazonaws.com/outline-releases/client/windows/stable/Outline-Client.exe">Windows</a>, <a href="https://apps.apple.com/us/app/outline-app/id1356178125">MacOS</a>\n\n"""\
          f"""<b>✅Шаг 2:</b> Скопируйте ваш ключ и вставьте в приложение Outline \n\n"""\
          f"""<b>✅Шаг 3:</b> Нажмите кнопку «Подключиться»\n"""

    return txt
