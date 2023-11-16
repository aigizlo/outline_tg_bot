import urllib3
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from outline_api import (

    Manager)

#Настройки бота
token = '6820291522:AAHbWTF-zSlL3bIdDqmjqSajYBsGbueRlQs'

bot_name = 'offradar_VPNbot'


# token = '6074035686:AAEWCJFAsnRdOBBRNNtl56Ef-wed8m-ucZg'
#
# bot_name = 'outlinexbot'
# #
support = "@off_radar_support"

# aiogram
bot = Bot(token=token)


storage = MemoryStorage()

dp = Dispatcher(bot, storage=storage)

# Указываем Merchant ID и Secret Key от AnyPay
merchant_id = '156CC3CBD6B66EFF7F'
secret_key = '5gu8fRE3dxWUzuIsrKCa3iV2e5UfvSe1T3tT7MO'
project_id = '12622'

# Указываем Merchant ID и Secret Key от Free_kassa

secret_word1 = 'DP.oy$a]CsVB=)B'
secret_word2 = '$w$79)98%^u9}tj'
free_kassa_merchant_id = '40657'


# fropay
secret_key_fropay = '9uxfltmav7or5q3'
public_key_fropay = 'e4896kmtqs3xvz0'
shop_id_fropay = '3510'


# данные для подлкючения к бд
host = "localhost"
user = "aigiz"
password = "Imaroot1"
database = "outline"

# данные для подключения к менеджеру outline
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# cервер номер 1 Nederland
apiurl_amsterdam = "https://212.118.53.231:40863/tUVEBiy0F8Qm8zyC8VXrjg"
apicrt_amsterdam = "744393954-c8cc-4d71-bbc0-378914440ed3"

# сервер номер 2 Germany
apiurl_germany = "https://89.208.103.199:3509/SmiTzdKTj715pmUI-2mCbg"
apicrt_germany = "adb4d844-ccf5-4a47-a2aa-008091a544fe"

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
apiurl_usa = 'https://95.181.173.94:8144/dWPpXIf-atl26uKXOIx11A'
apicrt_usa = '60c9b375-b206-40ca-a637-c6b911759e00'

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

# api_wallet = "boPvJGD9zMPvFUqVltLpe96sFF5lcd8pciC3"

# INSERT INTO server server_id = 6, name = 'Los Angeleg', country = 'USA';
