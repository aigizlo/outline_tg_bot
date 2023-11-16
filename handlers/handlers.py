from logger import logger
from aiogram.dispatcher import FSMContext

from logic_keys.add_keys import add_keys, add_free_keys
from user_data import UserData, check_user_in_system
from config import dp, bot, err_send, support
from keyboards.keyboards import *
from states import MyStates
from text import answer_error, text_free_tariff, instruction, promotion_text, instruction_and_main_menu

user_data = UserData()

amount_to_month = {
    1: one_month,
    2: two_month,
    3: three_month,
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
}

get_keys_handlers = ['🔐Получить еще ключ', '🔐Получить ключ']


# обрабатываем нажатие кнопки "Получить ключ"
@dp.message_handler(lambda message: message.text in get_keys_handlers, state="*")
async def get_key_command(message: types.Message, state: FSMContext):

    if not check_user_in_system(message.from_user.id):
        await message.answer("Что бы начать работу с ботом используйте команду /start")
        return

    # импортируем кливатуру
    user_info = user_data.get_userid_firsname_nickname(message.from_user.id)

    user_id = user_info[0]

    free_tarrif = user_data.free_tariff(user_id)

    keyboard = choice_period_not_free()

    if free_tarrif == "UNUSED":
        keyboard = choice_period()

    answer = "Выберите тариф:"
    # cur_state = await state.get_state()
    await state.set_state(MyStates.state_get_keys)

    logger.info(f"Получить ключ, user_id - {user_info}")

    await message.answer(answer, reply_markup=keyboard)

@dp.callback_query_handler(lambda c: c.data.startswith('get_keys:'), state='*')
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
        await state.update_data(user_id=user_id, action='pay', month=month, amount=amount)

        # удаляем клавиатуру с выбором тарифа для продления
        await bot.delete_message(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id)

        answer = f"Сумма покупки <b>{amount}</b> рублей, выберите способ оплаты:"

        # клава
        keyboard = get_pay_method_keyboard()

        await state.set_state(MyStates.pay_from_balance)

        logger.info(f'Покупка ключа , user - {user_info} на сумму {amount}, период - {month}')

        await bot.send_message(chat_id=callback_query.message.chat.id, text=answer, parse_mode='HTML',
                               reply_markup=keyboard)
    except Exception as e:
        logger.error(f"ERROR:Ошибка при продлении ключа, user - {user_info}, ошибка - {e}")
        await bot.send_message(answer_error, reply_markup=main_menu())



# обрабатываем нажатие кнопки "Назад"
@dp.message_handler(lambda message: message.text == '🔙Назад', state='*')
async def back_command(message: types.Message, state: FSMContext):
    user_info = user_data.get_userid_firsname_nickname(message.from_user.id)

    if not check_user_in_system(message.from_user.id):
        await message.answer("Что бы начать работу с ботом используйте команду /start")
        return
    User_Data = UserData()
    main_menu_kb = main_menu()
    logger.info(f"Назад user - {user_info}")

    await message.answer(instruction_and_main_menu, disable_web_page_preview=True,
                             parse_mode='HTML',
                             reply_markup=main_menu_kb)

    try:
        user_id = User_Data.get_user_id(message.from_user.id)

        if user_id:
            # проверяем использовал ли он бесплатный тариф
            if User_Data.free_tariff(user_id) == "UNUSED":
                await message.answer("Главное меню")
    except Exception as e:
        logger.error(f"ERROR: Назад, user - {user_info}, ошибка - {e}")
        answer = answer_error
        await message.answer(answer, reply_markup=main_menu_kb)
        await bot.send_message(err_send, f"Ошибка при нажатии НАЗАД - {e}, пользователь {user_info}")
    await state.finish()


# inline кнопка "Отмена"
@dp.callback_query_handler(lambda c: c.data == "go_back", state="*")
async def process_callback_go_back(callback_query: types.CallbackQuery):
    user_info = user_data.get_userid_firsname_nickname(callback_query.message.chat.id)
    await bot.answer_callback_query(callback_query.id)

    # Удаляем предыдущее сообщение с инлайн-клавиатурой
    await bot.delete_message(chat_id=callback_query.message.chat.id,
                             message_id=callback_query.message.message_id)
    logger.info(f"Отмена - user - {user_info}")


#
@dp.callback_query_handler(lambda c: c.data == "subscribe_ago", state="*")
async def check_subscription(callback_query: types.CallbackQuery):
    telegram_id = callback_query.from_user.id
    subscribe_keyboard = subscribe()

    user_info = user_data.get_userid_firsname_nickname(callback_query.message.chat.id)

    user_id = user_info[0]
    user_name = user_info[1]

    try:
        User_Data = UserData()

        # Выясняем, есть пользовался ли юзер бесплатным тарифом
        use_free_tariff = User_Data.free_tariff_tg(telegram_id)
        chat_member = await bot.get_chat_member(chat_id="@off_radar",
                                                user_id=telegram_id)

        if chat_member.status in ["member", "administrator", "creator", "owner"]:
            if use_free_tariff == "UNUSED":
                count_keys = user_data.get_keys_ids(user_id)
                count_keys = len(count_keys)
                if not count_keys:
                    count_keys = 0

                count_keys = count_keys + 1

                key_name = f"Ключ № {count_keys}"
                key_id = add_free_keys(user_id, key_name)

                if key_id:
                    key_value = User_Data.get_key_value(key_id)
                    answer = text_free_tariff(key_value)
                    User_Data.change_free_tariff(user_id, 1)
                else:
                    answer = answer_error
                await bot.send_message(chat_id=callback_query.from_user.id,
                                       text=answer, parse_mode="HTML", disable_web_page_preview=True)
                await bot.delete_message(chat_id=callback_query.message.chat.id,
                                         message_id=callback_query.message.message_id)
            else:
                await bot.delete_message(chat_id=callback_query.message.chat.id,
                                         message_id=callback_query.message.message_id)
        else:
            await bot.send_message(chat_id=callback_query.message.chat.id,
                                   text="Вы не подписаны на канал!",
                                   reply_markup=subscribe_keyboard)
    except Exception as e:
        logger.error(f'ERROR:PROCESSО - check_subscription - Ошибка при проверке на подписку {user_id}: {e}')
        await bot.send_message(err_send, f'ERROR:PROCESSО - check_subscription - Ошибка при проверке на подписку {user_id}: {e}')


@dp.message_handler(commands=['my_info'], state="*")
async def my_info(message: types.Message):
    try:
        user_info = user_data.get_userid_firsname_nickname(message.from_user.id)

        user_id = user_info[0]

        all_info = user_data.get_user_info(user_id)

        txt_user_id = f"Мой user_id : {user_id}\n"

        answer = txt_user_id + all_info

        await message.reply(answer, disable_web_page_preview=True,
                            parse_mode="HTML")
        logger.info(f"my_info command - user {user_id}")

    except Exception as e:
        logger.info(f"COMMAND_ERROR - /my_info, {e}")
        await message.reply(f"Произошла ошибка при получении информации о пользователе .{e}")


@dp.message_handler(commands=['help'], state="*")
async def my_info(message: types.Message):
    await message.reply(f"По всем вопросам - {support}")


@dp.message_handler(commands=['instruction'], state="*")
async def my_info(message: types.Message):
    await message.reply(instruction, parse_mode="HTML", disable_web_page_preview=True)
