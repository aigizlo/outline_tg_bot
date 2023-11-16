import json
from datetime import datetime

from user_data import execute_query

server_id_country_for_txt = {
    1: "🇳🇱<b>Ключи Нидерланды - Амстердам</b> :\n\n",
    2: "🇩🇪<b>Ключи Германии - Франкфурт</b> :\n\n",
    3: "🇹🇷<b>Ключи Kz - Стамбул</b> :\n\n",
    4: "🇷🇺<b>Ключи Россия - СПБ</b> :\n\n",
    5: "🇹🇷<b>Ключи Турция - Стамбул</b> :\n\n",
    6: "🇺🇸<b>Ключи Америка - Лос Анджелес</b> :\n\n"
}

def test_sql():
    sql = ''' SELECT      u.name,     o.server_id,     o.key_value,     u.stop_date FROM     outline_keys o LEFT JOIN
         user_keys u ON     o.key_id = u.key_id WHERE     u.user_id = 276'''

    result = execute_query(sql)



    return result

keys_lst1 = test_sql()

def keys_send(keys_lst):
    txt = ''

    unic_server_id = 0

    def text(name, key, date):
        text = f"""Название ключа <b>"{name}"</b>,\n - <code>{key}</code>\n(👆кликни для копирования)\n- ключ действителен до {date}\n\n"""

        return text

    def country_text(server_id, name, key, date):
        txt = server_id_country_for_txt.get(server_id)

        text = f"""Название ключа <b>"{name}"</b>,\n - <code>{key}</code>\n(👆кликни для копирования)\n- ключ действителен до {date}\n\n"""

        return txt + text



    for key_data in keys_lst:
        key_name = key_data[0]
        server_id = key_data[1]
        key_value = key_data[2]
        key_date = key_data[3].strftime('%d %B %Y')

        if unic_server_id == server_id:
            txt += text(key_name, key_value, key_date)
        else:
            txt += country_text(server_id,key_name, key_value, key_date)
            unic_server_id = server_id


    return txt







print(keys_send(keys_lst1))