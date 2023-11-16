import urllib3
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from outline_api import (

    Manager)

#Настройки бота
token = ''

bot_name = ''



# #
support = ""

# aiogram
bot = Bot(token=token)


storage = MemoryStorage()

dp = Dispatcher(bot, storage=storage)

# Указываем Merchant ID и Secret Key от AnyPay
merchant_id = '156CC3CBD6B66EFF7F'
secret_key = '5gu8fRE3dxWUzuIsrKCa3iV2e5UfvSe1T3tT7MO'
project_id = '12622'

# Указываем Merchant ID и Secret Key от Free_kassa

secret_word1 = 
secret_word2 = 
free_kassa_merchant_id = 


# fropay
secret_key_fropay = 
public_key_fropay = 
shop_id_fropay = 


# данные для подлкючения к бд
host = "localhost"
user = ""
password = ""
database = "outline"

# данные для подключения к менеджеру outline
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# cервер номер 1 Nederland
apiurl_amsterdam = ""
apicrt_amsterdam = ""

# сервер номер 2 Germany
apiurl_germany = ""
apicrt_germany = ""

# сервер номер 3 Kazahstan
apiurl_kz = "https://188.225.31.86:3768/23V3Fbs0ttuPiYWf1TCq5A"
apicrt_kz = "da6896f9-4f3e-47d5-b8b5-b4cec9aaf3cd"

# сервер номер 4 Sankt-Pirerburg
apiurl_spb = "https://45.153.69.147:23454/a4PAg9Ydh7yCSXTO5yBG6g"
apicrt_spb = "e540ff22-ace2-4d5a-8810-8786a34d38b0"

# сервер номер 5 Turkey
apiurl_turkey = "https://185.219.134.225:1719/FyENbYMQxz_W9UTK_sEnzA"
apicrt_turkey = "83e234a9-7b7e-4f95-b6de-7f0022e89de8"

# сервер номер 6 usa
apiurl_usa = ''
apicrt_usa = ''

manager_amsterdam = Manager(apiurl=apiurl_amsterdam, apicrt=apicrt_amsterdam)

manager_germany = Manager(apiurl=apiurl_germany, apicrt=apicrt_germany)

manager_kz = Manager(apiurl=apiurl_kz, apicrt=apicrt_kz)

manager_spb = Manager(apiurl=apiurl_spb, apicrt=apicrt_spb)

manager_turkey = Manager(apiurl=apiurl_turkey, apicrt=apicrt_turkey)

manager_usa = Manager(apiurl=apiurl_usa, apicrt=apicrt_usa)

managers = {
    1: manager_amsterdam,
    2: manager_germany,
    3: manager_kz,
    4: manager_spb,
    5: manager_turkey,
    6: manager_usa,
}

server_id_country = {
    1: '🇱🇺Нидерланды Амстердам',
    2: '🇩🇪Германия Франкфурт',
    3: '🇰🇿Казахстан Астана',
    4: '🇷🇺Россия',
    5: '🇹🇷Турция Стамбул',
    6: '🇺🇸Америка Лос Анджелес'
}




# коэфициент реферального бонуса
coefficeint_bonus = 0.2


# для партнеров реферальный бонус 50%
partners = [47, 68, 93]
partner_bonus = 0.5
# имеют доступ к админским командам
admin_from_config = [502811372, 1139164093, 235013345]
# уведомления об ошибках
err_send = 502811372


# цены
one_month = 149
two_month = 269
three_month = 380
six_month = 630


