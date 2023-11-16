from aiogram.dispatcher import FSMContext
from logger import logger
from logic_keys.add_keys import exchange_server
from config import support
from config import dp, bot
from keyboards.keyboards import *
from text import answer_error, answer_if_change
from states import MyStates
from user_data import UserData


user_data = UserData()


@dp.message_handler(lambda message: message.text == '🔁Сменить локацию VPN', state="*")
async def change_location_handlers(message: types.Message, state: FSMContext):
    telegram_id = message.from_user.id
    user_info = user_data.get_userid_firsname_nickname(telegram_id)
    user_id = user_info[0]

    keys_ids = user_data.get_keys_ids(user_id)

    count_keys = len(keys_ids)

    logger.info(f"(change_location_handlers) Сменить локацию user - {user_info}")

    # ищем юзер_айди пользователя
    try:
        if count_keys > 1:

            # получаем список имен ключей
            name_key = user_data.get_user_name_keys(user_id)
            if not user_data.get_user_name_keys(user_id):
                answer = "У вас нет ключей для смены их локации, нажмите «Назад»"
                await message.answer(answer)
                keyboard = back_button()
                await message.answer(answer, reply_markup=keyboard)
                return
            # если есть ключи, то генерируем кнопки с их названиями
            key_buttons = generate_key_buttons_for_exchange(name_key)
            answer = "Выберите ключ, у которого хотите сменить локацию :"

            await state.set_state(MyStates.state_key_exchange)

            # Первое сообщение с инлайн-клавиатурой
            await message.answer(answer, reply_markup=key_buttons)

        else:

            servers = user_data.get_used_server_id()
            key_id = keys_ids[0][0]
            current_server = user_data.get_current_used_server(keys_ids[0][0])
            current_server = current_server[0][0]
            servers = [item[0] for item in servers]
            servers.remove(current_server)
            # генерим кнопки названия серверов
            keyboard = generate_location_button(servers)

            answer = "ВНИМАНИЕ‼️\n" \
                     "При смене локации вам будет предоставлен новый ключ, с новой локацией. " \
                     "Старый ключ будет неактивен!\n\n" \
                     "Выберите новую локацию:"
            await message.answer(answer, reply_markup=keyboard)
            await state.set_state(MyStates.state_key_exchange)
            await state.update_data(key_id=key_id)

    except Exception as e:
        logger.error(f"(change_location_handlers)ERROR:Смена локации user - {user_info} ошибка - {e}")
        await message.answer(answer_error, reply_markup=main_menu())


# Меняем локацию
@dp.callback_query_handler(lambda c: c.data.startswith("select_country_for_exchange"), state=MyStates.state_key_exchange)
async def choosing_new_location(callback_query: types.CallbackQuery, state: FSMContext):
    telegram_id = callback_query.from_user.id
    user_info = user_data.get_userid_firsname_nickname(telegram_id)

    # выбранный сервер для смены локаций
    selected_server = callback_query.data.split(":")[1]
    user_data_state = await state.get_data()



    try:
        key_id = user_data_state['key_id']

        location = server_id_country.get(int(selected_server))

        logger.info(f"(choosing_new_location) Выбрана новая локация {location}, user - {user_info}")

        await bot.delete_message(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id)

        new_key = exchange_server(key_id, selected_server)

        if not new_key:
            answer = f"Произошла ошибка, обратитесь к администратору - {support}"

            await bot.send_message(telegram_id, answer)

            logger.info(f"Ошибка при смене локации user - {user_info}")

            return

        answer = answer_if_change(new_key, location)

        await bot.send_message(telegram_id, answer, parse_mode="HTML", disable_web_page_preview=True)
    except Exception as e:
        logger.error(f'(choosing_new_location) Ошибка при выборе новой локации - {e}')


# Выбраный ключ для смены локации
@dp.callback_query_handler(lambda c: c.data.startswith("selecting_key_for_exchange"), state=MyStates.state_key_exchange)
async def select_key_for_exchange(callback_query: types.CallbackQuery, state: FSMContext):
    telegram_id = callback_query.from_user.id
    user_info = user_data.get_userid_firsname_nickname(telegram_id)

    user_id = user_info[0]

    selected_key = callback_query.data.split(":")[1]

    logger.info(f"(select_key_for_exchange)Выбран ключ - {selected_key} для его смены, user - {user_info}")

    try:
        key_id = user_data.get_key_id_with_key_name_and_user_id(selected_key, user_id)

        await bot.delete_message(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id)

        await state.update_data(key_id=key_id)

        servers = user_data.get_used_server_id()

        servers = [item[0] for item in servers]

        keyboard = generate_location_button(servers)

        answer = f"Вы выбрали {selected_key}\nВыберите новую локацию:"

        await bot.send_message(telegram_id, answer, reply_markup=keyboard)
    except Exception as e:
        logger.error(f'(select_key_for_exchange) ошибка при выборе ключа для его смены user - {user_info}, {e}')
