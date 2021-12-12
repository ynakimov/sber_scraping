"""
Скраппинг курсов драгоценных металлов на сайте sberbank.ru
"""

# from urllib.parse import urlparse
# from bs4 import BeautifulSoup
import csv
import json
import datetime
import requests
from fake_useragent import UserAgent
from plotly.graph_objs import Bar, Layout

from plotly import offline
import plotly.graph_objs as go
import plotly.express as px
from plotly.subplots import make_subplots

import pandas as pd
import database as db


HEADERS_SBER_BANK = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:94.0) Gecko/20100101 Firefox/94.0',
}


def save_as_readable_json(text, file_path):
    """ Для отладки получим ридабельное представление json """
    readable_file_path = 'readable_data_20211208.json'
    with open(file_path, 'w') as f:
        json.dump(text, f, indent=4)


def get_data(getted_result):
    """ Обработка данных запрошеннного URL, полученение json  в виде словаря """  
    result = {}  
    result['status'] = getted_result.status_code
    if getted_result.status_code == 200:
        result['json'] = getted_result.json()    
    else:
        result['json'] = {}    
    return result


def get_request(rateType, isoCodes, millisecond):
    """ Получает результат запроса ресурса URL """
    ua = UserAgent()
    headers = HEADERS_SBER_BANK.copy()
    headers['User-Agent'] = ua.random
    full_url = 'https://www.sberbank.ru/proxy/services/rates/public/history?rateType={}&isoCodes[]={}&date={}&regionId=038'.format(rateType, isoCodes, millisecond)
    result = requests.get(full_url, headers=headers, allow_redirects=True)
    return result


def average_per_day(dict_of_rates):
    """ Средние цены продажи/покупки за день"""
    summaSell = 0
    summaBuy = 0  
    count = 0
    for key, val in dict_of_rates.items():
        # print(key)
        count += 1
        for v in val["rangeList"]:
            if v["rangeAmountBottom"] == 0:
                summaSell += v['rateSell'] 
                summaBuy += v['rateBuy']
                # print(v)

    averageSell = int(summaSell/count)
    averageBuy = int(summaBuy/count)
    return {'price_sell': averageSell, 'price_buy': averageBuy}   


def get_data_to_dictionary_for_period(begin_date, rateType, isoCodes, structure='for_csv'):
    """ Возвращает данные сайта за период с current_date (самая ранняя 21-06-2021) и по текущую дату.
        В зависимости от structure возвращает либо список словарей (когда structure ='for_csv') 
        либо словарь списков """

    if structure =='for_csv':
        price_by_date = []
    else:
        dates = []
        prices_sell = []
        prices_buy = []          
        price_by_date = {'dates': dates, 'prices_sell': prices_sell, 'prices_buy': prices_buy}        

    # current_date = datetime.datetime(2021, 6, 21)
    current_date = datetime.datetime(begin_date.year, begin_date.month, begin_date.day)
    timedelta = datetime.timedelta(1)
        
    today     = datetime.date.today()
    end_date  = datetime.datetime(today.year, today.month, today.day)
    while current_date <= end_date:
        weekday = current_date.weekday()
        if weekday < 5:
            millisecond = int(current_date.timestamp() * 1000)
            millisecond = str(millisecond)             
            getted_result  = get_request(rateType, isoCodes, millisecond)
            data = get_data(getted_result)
            if data['status'] == 200:
                # data = get_data(getted_result)
                metal_exchange_rates = data['json']
                dict_of_rates = metal_exchange_rates['historyRates'][millisecond][rateType][isoCodes]
                price = average_per_day(dict_of_rates)
                if structure == 'for_csv':
                    date_dict = {}
                    date_dict['date'] = current_date.date()                
                    date_dict['price_sell'] = price['price_sell']
                    date_dict['price_buy'] = price['price_buy']
                    price_by_date.append(date_dict)
                else:
                    dates.append(current_date.date())
                    prices_sell.append(price['price_sell'])
                    prices_buy.append(price['price_buy'])

            else:
                print(f'Ошибка получения данных сайта за {data} ')      
            # print(f'millisecond = {millisecond}')
            print(current_date.date())                        
        current_date = current_date + timedelta
    
    if structure != 'for_csv':
        price_by_date['dates'] = dates
        price_by_date['prices_sell'] = prices_sell
        price_by_date['prices_buy'] = prices_buy
            
    return price_by_date


def save_as_csv(price_by_date, filename):
    with open(filename, 'x', newline='') as csvfile:
        # writer = csv.writer(f, dialect='excel')
        fieldnames = ['date', 'price']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, dialect='excel')
        writer.writeheader()
        for item in price_by_date:
            writer.writerow(item)


def show_diagram(price_data):
    fig = go.Figure()
    mode='lines+markers'
    fig.add_trace(go.Scatter(x=price_data['dates'], y=price_data['prices_sell'], mode=mode, name='prices of sell'))
    fig.add_trace(go.Scatter(x=price_data['dates'], y=price_data['prices_buy'], mode=mode, name='prices of buy'))
    fig.update_yaxes(title='Цена, руб.')
    fig.update_layout(title="Цены покупки/продажи ОМС (золото) на сайте Сбербанка")
    fig.update_traces(hoverinfo="all", hovertemplate="Дата: %{x}<br>Цена: %{y}")
    fig.show()



# filename = 'price_by_date.csv'
# save_as_csv(price_by_date, filename)

# getted_result  = get_request('ERNP-6', 'USD', 1638997200000)
# data = get_data(getted_result)

# exchange_rates = data['json']

# millisecond = str(DATA_MILLISECUND)
# dict_of_rates = exchange_rates['historyRates'][millisecond][CLIENT_LAVEL][METALL_COD]

# print(average_per_day(dict_of_rates, millisecond))
# file_path = 'readable_USD_20211209.json'
# save_as_readable_json(exchange_rates, file_path)


# d = 2