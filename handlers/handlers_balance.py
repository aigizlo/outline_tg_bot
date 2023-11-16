from create_pay_links import generate_any_pay_link, generate_fropay_link
from balance import creating_payment
from logger import logger
from aiogram.dispatcher import FSMContext
from config import dp, secret_key, bot
from keyboards.keyboards import *
from states import MyStates
from text import answer_error
from user_data import UserData, check_user_in_system

user_data = UserData()


# обрабатываем нажатие кнопки "Баланс"
@dp.message_handler(lambda message: message.text == '💰Баланс', state='*')
async def balance_command(message: types.Message, state: FSMContext):
    user_info = user_data.get_userid_firsname_nickname(message.from_user.id)

    if not check_user_in_system(message.from_user.id):
        await message.answer("Что бы начать работу с ботом используйте команду /start")
        return

    try:
        keyboard = balance_keyboard()

        # забираем из класса UserData
        user_id = user_info[0]

        await state.update_data(user_id=user_id)

        user_balance = user_data.get_user_balance_ops_by_user_id(user_id)

        answer2 = f"Ваш баланс {user_balance} рублей"

        logger.info(f"Баланс, user - {user_info}")
        # await state.set_state(MyStates.state_balance)
        await message.answer(answer2, reply_markup=keyboard)
    except Exception as e:
        logger.error(f"ERROR:Баланс, user_id - {user_info}, error - {e}")
        await message.answer(answer_error, reply_markup=main_menu())


@dp.message_handler(lambda message: message.text == 'Пополнить баланс', state="*")
async def replenish_balance_comand(message: types.Message, state: FSMContext):
    user_info = user_data.get_userid_firsname_nickname(message.from_user.id)
    await message.answer("Выберите сумму, на которую хотите ваш баланс, или напишите свою сумму", reply_markup=kb_inline_prices())
    await state.set_state(MyStates.state_replenish_balance)
    logger.info(f"Пополнить баланс, user - {user_info}")


# получаем сумму, для пополнения
@dp.message_handler(state=MyStates.state_replenish_balance)
async def get_amount_for_payment(message: types.Message, state: FSMContext):
    amount_str = message.text
    user_info = user_data.get_userid_firsname_nickname(message.from_user.id)
    user_data_state = await state.get_data()
    user_id = user_data_state["user_id"]

    amount = int(amount_str)

    # создаем платеж и генерируем pay_id
    pay_id = creating_payment(amount, user_id)

    desc = f'{user_id},{amount},{pay_id}'

    try:
        if isinstance(amount, int):
            # генерируем ссылку для оплаты
            any_pay_link = generate_any_pay_link(str(pay_id), desc, str(amount), secret_key)
            # вставляем ссылку в инлайн кнопку

            fropay_link = generate_fropay_link(str(pay_id), str(amount))
            keyboard = kb_pay(amount, any_pay_link, fropay_link)
            # отправляем пользователя
            await message.answer(f"Выберите платежную систему для оплаты {amount} рублей.",
                                 reply_markup=keyboard)
            logger.info(f"Пополнить баланс на сумму - {amount}, user - {user_info}")  #

        else:
            await message.answer("Введенное значение не является целым числом.")
    except ValueError as e:

        logger.error(f"ERROR:Пополнить баланс на сумму - {amount}, user - {user_info}, ошибка - {e}")

        await message.answer("Произошла ошибка, пожалуйста, обратитесь к администратору")


@dp.callback_query_handler(lambda c: c.data.startswith('pr:'), state='*')
async def get_amount_for_payment_2(callback_query: types.CallbackQuery):
    try:
        telegram_id = callback_query.from_user.id
        user_info = user_data.get_userid_firsname_nickname(telegram_id)
        user_id = user_info[0]

        amount = int(callback_query.data.split(':')[1])
        pay_id = creating_payment(amount, user_id)

        desc = f'{user_id},{amount},{pay_id}'
        any_pay_link = generate_any_pay_link(str(pay_id), desc, str(amount), secret_key)
        # вставляем ссылку в инлайн кнопку
        fropay_link = generate_fropay_link(str(pay_id), str(amount))
        keyboard = kb_pay(amount, any_pay_link, fropay_link)

        await bot.delete_message(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id)

        logger.info(f"Пополнить баланс на сумму - {amount}, user - {user_info}")  #
        await bot.send_message(chat_id=callback_query.message.chat.id, text="Выберите платежную систему для оплаты", parse_mode='HTML',
                               reply_markup=keyboard)
    except Exception as e:
        logger.error(f"ERROR:Пополнить баланс на сумму - {amount}, user - {user_info}, ошибка - {e}")
        await bot.send_message(answer_error, reply_markup=main_menu())
