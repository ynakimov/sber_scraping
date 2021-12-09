"""
Скраппинг курсов драгоценных металлог сайта sberbank.ru
"""

from urllib.parse import urlparse
# from bs4 import BeautifulSoup
import json
import datetime
import requests
from fake_useragent import UserAgent
import csv

HEADERS_SBER_BANK = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:94.0) Gecko/20100101 Firefox/94.0',
}

FULL_URL = 'https://www.sberbank.ru/proxy/services/rates/public/history?rateType=PMR-4&isoCodes[]=A98&date=1638219600000&regionId=038'
FULL_URL = 'https://www.sberbank.ru/proxy/services/rates/public/history?rateType=PMR-4&isoCodes[]=A98&date=1638910800000&regionId=038'


CLIENT_LAVEL ='PMR-4'
METALL_COD = 'A98' # Металл 98 - золото, 99 - серебро
DATA_MILLISECUND = 1638910800000


def save_as_readable_json(text):
    """ Для отладки получим ридабельное представление json """
    readable_file_path = 'readable_data_20211208.json'
    with open(readable_file_path, 'w') as f:
        json.dump(text, f, indent=4)


def get_data(getted_result):
    """ Обработка данных запрошеннного URL, полученеие json  в виде словаря  """  
    result = {}  
    result['status'] = getted_result.status_code
    if getted_result.status_code == 200:
        result['json'] = getted_result.json()    
    else:
        result['json'] = {}    
    return result


def get_request(client_rating, metall_cod, millisecond):
    """ Получает результат запроса ресурса"""
    ua = UserAgent()
    headers = HEADERS_SBER_BANK.copy()
    headers['User-Agent'] = ua.random
    full_url = 'https://www.sberbank.ru/proxy/services/rates/public/history?rateType={}&isoCodes[]={}&date={}&regionId=038'.format(client_rating, metall_cod, millisecond)
    result = requests.get(full_url, headers=headers, allow_redirects=True)
    return result


def average_per_day(dict_of_rates, millisecond):
    """ Средняя цена продажи за день"""
    summa = 0 
    count = 0
    for key, val in dict_of_rates.items():
        # print(key)
        count += 1
        for v in val["rangeList"]:
            if v["rangeAmountBottom"] == 0:
                summa += v['rateSell'] 
                # print(v)

    average = round(summa/count, 2)
    return average   

date = []
price = []

def get_data_for_period():
    """ Возвращает данные сайта за период с 21-06-2021 по текущую дату """

    current_date = datetime.datetime(2021,6,21)
    timedelta = datetime.timedelta(1)
    today     = datetime.date.today()
    end_date  = datetime.datetime(today.year, today.month, today.day)
    # date_today = datetime.date.today()
    while current_date <= end_date:
        # Возвращает день недели в виде целого числа, где понедельник равен 0, а воскресенье-6.

        weekday = current_date.weekday()
        if weekday < 5:
            millisecond = int(current_date.timestamp() * 1000)
            millisecond = str(millisecond)             
            getted_result  = get_request(CLIENT_LAVEL, METALL_COD, millisecond)
            data = get_data(getted_result)
            if data['status'] == 200:
                date_dict = {}
                date_dict['date'] = current_date.date()
                date_dict['millisecond'] = millisecond                
                date.append(date_dict)

                data = get_data(getted_result)
                metal_exchange_rates = data['json']
                dict_of_rates = metal_exchange_rates['historyRates'][millisecond][CLIENT_LAVEL][METALL_COD]
                price.append(average_per_day(dict_of_rates, millisecond))
            else:
                print(f'Ошибка получения данных сайта за {data} ')      
            print(f'millisecond = {millisecond}')
            print(current_date.date())                        
        current_date = current_date + timedelta


# getted_result  = get_request(FULL_URL, CLIENT_LAVEL, METALL_COD, DATA_MILLISECUND)
# data = get_data(getted_result)

# metal_exchange_rates = data['json']
# millisecond = str(DATA_MILLISECUND)
# dict_of_rates = metal_exchange_rates['historyRates'][millisecond][CLIENT_LAVEL][METALL_COD]

# print(average_per_day(dict_of_rates, millisecond))
get_data_for_period()


d = 2