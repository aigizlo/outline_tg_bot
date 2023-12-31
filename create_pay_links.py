import urllib.parse
import hashlib

def generate_fropay_link(payment_id, amount):
    # переводим сумму в формат 123.00
    amount = amount + ".00"
    public_key_fropay = 'e4896kmtqs3xvz0'
    shop_id_fropay = '3510'

    # формируем строку для генерации хэша
    hash_string = f'{shop_id_fropay}{amount}{public_key_fropay}{payment_id}'

    # генерируем хэш
    payment_hash = hashlib.sha256(hash_string.encode('utf-8')).hexdigest()

    # формируем ссылку для оплаты
    payment_link = f'https://sci.fropay.bid/get?amount={amount}&desc=MTAyMTU=&shop_id={shop_id_fropay}&label={payment_id}&hash={payment_hash}'

    return payment_link


def generate_any_pay_link(pay_id, desc, amount, secret_key):
    project_id = '12622'
    currency = 'RUB'
    success_url = ''
    fail_url = ''

    params = {
        'merchant_id': project_id,
        'pay_id': pay_id,
        'amount': amount,
        'currency': currency,
        'desc': desc,
        'success_url': success_url,
        'fail_url': fail_url
    }

    arr_sign = [project_id, pay_id, amount, currency, desc, success_url, fail_url, secret_key]

    # подпись
    sign = hashlib.sha256(":".join(arr_sign).encode()).hexdigest()

    # params['sign'] = sign
    encoded_params = urllib.parse.urlencode(params)

    # подпись к параметрам
    encoded_params += f'&sign={sign}'

    # итоговая ссылка
    payment_url = f"https://anypay.io/merchant?{encoded_params}"

    return payment_url
