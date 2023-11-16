from aiogram.dispatcher import FSMContext
from logger import logger
from text import instruction, answer_not_keys
from config import dp, bot, err_send
from balance import pay_from_personal_balance, add_referral_bonus
from keyboards.keyboards import *
from logic_keys.add_keys import add_keys, keys_send, get_minimum_used_server
from logic_keys.renewal_keys import renewal_keys
from text import answer_if_buy, answer_if_not_balance, answer_error
from states import MyStates
from user_data import UserData, check_user_in_system
from balance import money_back

amount_to_month = {
    1: one_month,
    2: two_month,
    3: three_month,
    6: six_month
}
# для тестов
#
#
# amount_to_days = {
#     149: 0,
#     269: 1,
#     405: 2,
#     810: 3
# }

amount_to_days = {
    one_month: 31,
    two_month: 62,
    three_month: 93,
    six_month: 184
}


user_data = UserData()


# мои ключи
@dp.message_handler(lambda message: message.text == '🔑Мои ключи', state='*')
async def my_keys_command(message: types.Message, state: FSMContext):

    if not check_user_in_system(message.from_user.id):
        await message.answer("Что бы начать работу с ботом используйте команду /start")
        return
    telegram_id = message.from_user.id

    FLAG = False

    user_info = user_data.get_userid_firsname_nickname(telegram_id)

    await state.set_state(MyStates.state_my_keys)

    # ищем юзер_айди пользователя
    try:
        user_id = user_data.get_user_id(telegram_id)
        # получаем список имен ключей
        name_key = user_data.get_user_name_keys(user_id)
        # создаем 2 клавиатуры 1 c кнопкой "Назад" и 'Продлить ключи' если ключи есть у пользователя 2ую - если ключи есть
        keyboard = back_and_prolong_button()

        keyboard_not_keys = back_and_buy_button()

        # список всех ключей с названием и датой работы
        try:
            keys = user_data.get_user_keys_info(user_id)

            answer = keys_send(keys)

            # если ключей нет то пише что их нет
            if not answer:
                answer = answer_not_keys
                FLAG = True

            logger.info(f"Мои ключи user - {user_info}")

            # выбор клавиатуры в зависимости от условия
            reply_keyboard = keyboard_not_keys if name_key == [] else keyboard

            await message.answer(answer, parse_mode='HTML',
                                 disable_web_page_preview=True,
                                 reply_markup=reply_keyboard)
            if not FLAG:
                await message.answer(instruction,
                                     parse_mode='HTML',
                                     disable_web_page_preview=True,
                                     reply_markup=reply_keyboard)
        except Exception as e:
            logger.error(f"{e}")
    except Exception as e:
        logger.error(f"ERROR:Мои ключи, user - {user_info}, ошибка - {e}")
        await message.answer(answer_error, reply_markup=main_menu())


# Продлить ключи                                                              здесь ловим состояние
@dp.message_handler(lambda message: message.text == '⌛️Продлить действие ключей', state="*")
async def prolong_key_command(message: types.Message, state: FSMContext):
    telegram_id = message.from_user.id
    user_info = user_data.get_userid_firsname_nickname(telegram_id)

    # ищем юзер_айди пользователя
    try:
        user_id = user_info[0]
        # получаем список имен ключей
        name_key = user_data.get_user_name_keys(user_id)

        if not user_data.get_user_name_keys(user_id):
            answer = "У вас нет ключей для их продления, нажмите «Назад»"
            await message.answer(answer)
            keyboard = back_button()
            await message.answer(answer, reply_markup=keyboard)
            return
        # если есть ключи, то генерируем кнопки с их названиями
        key_buttons = generate_key_buttons(name_key)
        answer = "Выберите ключ, который хотите продлить :"
        logger.info(f"Продлить колючи user - {user_info}")

        # Первое сообщение с инлайн-клавиатурой
        await message.answer(answer, reply_markup=key_buttons)

    except Exception as e:
        logger.error(f"ERROR:Продлить колючи user - {user_info} ошибка - {e}")
        await message.answer(answer_error, reply_markup=main_menu())


# Выюираем какой ключ будет продлен
@dp.callback_query_handler(lambda c: c.data.startswith("select_key"), state='*')
async def process_select_key(callback_query: types.CallbackQuery, state: FSMContext):
    telegram_id = callback_query.from_user.id
    user_info = user_data.get_userid_firsname_nickname(telegram_id)
    try:
        # выбранный ключ для продления
        selected_key = callback_query.data.split(":")[1]

        # сохраняем этот ключ в память состояния
        await state.update_data(key_name=selected_key)
        # текущее состояние
        logger.info(f"Выбран ключ для продления - {selected_key}, user - {user_info}")

        # удаляем инлайн клавиатуру по выбору ключей
        await bot.delete_message(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id)

        # выводим клавиатуру, где юзер выбираем период продления
        keyboard = choice_renewal_period()

        await bot.send_message(callback_query.from_user.id,
                               f"Выберите период, на который хотите продлить ваш ключ: <b>{selected_key}</b>",
                               parse_mode='HTML',
                               reply_markup=keyboard)
        # передаем данные в новое состояние
        await state.set_state(MyStates.state_key_for_renewal)

        await bot.answer_callback_query(callback_query.id)

    except Exception as e:
        logger.error(f"ERROR: НЕ Выбран ключ для продления - {selected_key}, user - {user_info}, "
                     f"user - {telegram_id}, ошибка {e}")
        await bot.send_message(answer_error, reply_markup=main_menu())


@dp.callback_query_handler(lambda c: c.data.startswith('renewal:'), state=MyStates.state_key_for_renewal)
async def renewal_process(callback_query: types.CallbackQuery, state: FSMContext):
    telegram_id = callback_query.from_user.id

    user_info = user_data.get_userid_firsname_nickname(telegram_id)

    try:
        # Получаем данные из callback_data, месяц
        month = int(callback_query.data.split(':')[1])

        # формируем сумму от количества месяцев
        amount = amount_to_month.get(month, None)

        user_id = user_info[0]

        # обновляем данные состояния, и обозначаем, что это продление
        await state.update_data(user_id=user_id, action='renewal', month=month)

        # удаляем клавиатуру с выбором тарифа для продления
        await bot.delete_message(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id)

        answer = f"Сумма покупки <b>{amount}</b> рублей, выберите способ оплаты:"

        # клава
        keyboard = get_pay_method_keyboard()

        await state.set_state(MyStates.pay_from_balance)

        logger.info(f"Продление ключа , user - {user_info} на сумму {amount}, период - {month}")

        await bot.send_message(chat_id=callback_query.message.chat.id, text=answer, parse_mode='HTML',
                               reply_markup=keyboard)
    except Exception as e:
        logger.error(f"ERROR:Ошибка при продлении ключа, user - {user_info}, ошибка - {e}")
        await bot.send_message(answer_error, reply_markup=main_menu())


# обрабатываем клавиатуру get_pay_method_keyboard
@dp.callback_query_handler(lambda c: c.data.startswith("balance_pay_sever"), state=MyStates.pay_from_balance)
async def payment_from_balance(callback_query: types.CallbackQuery, state: FSMContext):
    telegram_id = callback_query.from_user.id
    user_info = user_data.get_userid_firsname_nickname(telegram_id)

    # берем переменные от этого состояния
    user_data_state = await state.get_data()  # Изменено с get_state() на get_data()
    # выясняем, покупка это или продление
    action = user_data_state["action"]

    user_id = user_info[0]
    current_balance = user_data.get_user_balance_ops_by_user_id(user_id)
    keyboard = main_menu()

    try:
        # определяем, что это покупка
        if action == 'pay':
            # сумма
            amount = int(user_data_state["amount"])

            # проверяем если средства для оплаты
            if amount > current_balance:
                answer = answer_if_not_balance
                logger.info(f"NONE_BALANCE - нехватка средства user - {user_info}, cумма покупки {amount}")
                await bot.send_message(chat_id=telegram_id, text=answer, reply_markup=kb_inline_prices())
                return

            result_pay = pay_from_personal_balance(user_id, amount)
            # проводим покупку

            if not result_pay:
                answer = answer_error
                logger.info(f"PAYMENT ERROR - ошибка при оплате у user - {user_info}, cумма покупки {amount}")
                await bot.send_message(chat_id=telegram_id, text=answer, reply_markup=keyboard)
                return

            # определяем дни от суммы покупки
            days = amount_to_days.get(amount, None)

            # выдаем минимально загруженный сервер
            server_id = get_minimum_used_server()

            count_keys = user_data.get_keys_ids(user_id)

            count_keys = len(count_keys)

            if not count_keys:
                count_keys = 0

            count_keys = count_keys + 1

            key_name = f"Ключ № {count_keys}"

            key_id = add_keys(server_id, user_id, key_name, days)
            logger.info(f"{key_id} - key_id")
            logger.info(
                f"Оплата, user - {user_info}, server - {server_id},сумма - {amount}")
            # если key_id не вернулся
            if not key_id:
                answer = answer_error
                # возвращаем средства
                if not money_back(user_id, amount):
                    logger.error(
                        f"MONEY BACK - ERROR - средства НЕВОЗВРАЩЕНЫ на баланс user - {user_info}, cумма {amount}")
                logger.info(
                    f"MONEY BACK - SUCSSESS - возвращены средства на баланс uuser - {user_info}, cумма {amount}")

                await bot.send_message(err_send,
                                       f"MONEY BACK - ERROR - средства НЕВОЗВРАЩЕНЫ на баланс user - {user_info}, "
                                       f"cумма {amount}")
                await bot.send_message(chat_id=telegram_id,
                                       text=answer,
                                       reply_markup=keyboard)
                return

            # достаем сам ключ для отправки
            key_value = user_data.get_key_value(key_id)
            # при успешном списании и получении ключа начисляем реферальный бонус
            referer_user_id = user_data.get_referrer_user_id(user_id)
            if user_data.get_referrer_user_id(user_id):
                referer_telegram = user_data.get_tg_if_use_user_id(referer_user_id)
                if not add_referral_bonus(user_id, amount):
                    await bot.send_message(chat_id=err_send,
                                           text=f"Не удалось начислить реферальный бонус пользователю {user_id}")
                try:
                    await bot.send_message(referer_telegram, f'Вам начислен реферальный бонус {amount * 0.2} рублей')
                except:
                    pass
            # если покупка прошла успешно, ты высылаем ему ключ

            location = server_id_country.get(server_id)

            answer = answer_if_buy(key_value, location)

            # удаляем предыдущее сообщение
            await bot.delete_message(chat_id=telegram_id,
                                     message_id=callback_query.message.message_id)

            await bot.send_message(chat_id=telegram_id,
                                   text=answer,
                                   parse_mode="HTML",
                                   disable_web_page_preview=True,
                                   reply_markup=keyboard)

            await state.finish()  # или await state.set_state("another_state")

        # если это продление, а не покупка
        if action == "renewal":
            # период на которое продлевается ключ
            month = user_data_state["month"]
            # имя ключа
            key_name = user_data_state["key_name"]
            # сумма покупки
            amount = amount_to_month.get(month, None)
            logger.info(
                f"PROCESS:Оплата продления , user - {user_info}, key_name -  {key_name}, сумма -  {amount}")

            if amount > current_balance:
                answer = answer_if_not_balance
                logger.info(
                    f"NONE_BALANCE - нехватка средств при продлении user - {user_info}, cумма покупки {amount}")
                await bot.send_message(chat_id=telegram_id, text=answer, reply_markup=kb_inline_prices())
                return

            if not pay_from_personal_balance(user_id, amount):
                answer = answer_error
                logger.info(f"PAYMENT ERROR - ошибка при продлении ключа у user - {user_info}, cумма покупки {amount}")
                await bot.send_message(chat_id=telegram_id, text=answer, reply_markup=keyboard)
                return

            if not renewal_keys(user_id, key_name, month):
                await bot.send_message(chat_id=telegram_id, text=answer_error, reply_markup=keyboard)
                if not money_back(user_id, amount):
                    await bot.send_message(err_send, f"Ошибка возврата средств на баланс user - {user_info},cумма {amount}")
                return

            if user_data.get_referrer_user_id(user_id):
                if not add_referral_bonus(user_id, amount):
                    await bot.send_message(chat_id=err_send,
                                           text=f"Не удалось начислить реферальный бонус пользователю {user_id}")

            answer = f"Продления ключа \"<b>{key_name}</b>\" прошло успешно👌!\nСпасибо, что выбрали <b>«Off Radar»!!</b> 😇"
            keyboard = main_menu()
            await bot.delete_message(chat_id=callback_query.message.chat.id,
                                     message_id=callback_query.message.message_id)
            await bot.send_message(chat_id=callback_query.message.chat.id, text=answer, parse_mode="HTML",
                                   reply_markup=keyboard)

            await state.finish()  # или await state.set_state("another_state")

    except Exception as e:
        logger.error(f"ERROR:Ошибка при оплате покупки или продления, user - {user_info}, ошибка - {e}")
        await bot.send_message(telegram_id, answer_error, reply_markup=main_menu())
        await bot.send_message(err_send, f"ERROR:Ошибка при оплате покупки или продления, user - {user_info}, ошибка - {e}")



