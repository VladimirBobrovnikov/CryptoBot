from utils import *
import random
import json
import requests


class ExceptionValue(Exception):
    pass


class ExceptionCurrency(Exception):
    pass


class ExceptionSameData(Exception):
    pass


class Convertator:

    @staticmethod
    def get_price(text):
        try:
            input_data = text.split()
            if len(input_data) != 3:
                raise ExceptionValue('Некорректный ввод данных')
            amount = float(input_data[2])
        except ExceptionValue as e:
            print(e, 'Нужна помощь? Введите /help', sep='\n')
            return e, None, None, None, None
        except ValueError:
            print('Неправильно указано количество\nНужна помощь? Введите /help', sep='\n')
            e = 'Некорректное значение количества'
            return e, None, None, None, None
        else:
            try:
                base, quote = chek_values(input_data[0], input_data[1])
                if base == quote:
                    raise ExceptionSameData('Вы дважды ввели одну валюту')
                keys = f'{base}_{quote}'
                URL = f'https://free.currconv.com/api/v7/convert?q={keys}&compact=ultra&apiKey=2aa2e9be16b043d76fd0'
                r = requests.get(URL)
                answer = json.loads(r.content)
                value = float(answer[keys]) * amount
                return None, input_data[0], input_data[1], amount, value
            except ExceptionCurrency as e:
                print(e, 'Нужна помощь? Введите /help', sep='\n')
                return e, None, None, None, None
            except ExceptionSameData as e:
                print(e, 'Нужна помощь? Введите /help', sep='\n')
                return e, None, None, None, None
            except Exception:
                e = 'ServerError'
                print(e)
                return e, None, None, None, None


def chek_values(data1, data2):
    if data1 not in KEYS_OFTEN_USED.keys():
        if data1 not in KEYS["results"].keys():
            raise ExceptionCurrency(f'Значение валюты {data1}, которую ты хочешь купить мне неизвестно')
        else:
            base = data1
    else:
        base = KEYS_OFTEN_USED[data1]

    if data2 not in KEYS_OFTEN_USED.keys():
        if data2 not in KEYS["results"].keys():
            raise ExceptionCurrency(f'Значение валюты {data2}, которую ты хочешь купить мне неизвестно')
        else:
            quote = data2
    else:
        quote = KEYS_OFTEN_USED[data2]
    return base, quote

def random_keys():
    return random.choice(list(KEYS["results"].keys()))

def random_tikers():
    text = ''
    for _ in range(5):
        tiker = random_keys()
        text = text + f'Валюта {KEYS["results"][tiker]["currencyName"]} имеет тикер {tiker}\n'
    return text
