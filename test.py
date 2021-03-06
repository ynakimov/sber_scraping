import datetime
import time

# td = datetime.datetime.today()
# print(f"td{td}")
FULL_URL = 'https://www.sberbank.ru/proxy/services/rates/public/history?rateType=PMR-4&isoCodes[]=A98&date=1638219600000&regionId=038'
FULL_URL     = 'https://www.sberbank.ru/proxy/services/rates/public/history?rateType=PMR-4&isoCodes[]=A98&date=1638910800000&regionId=038'
URL_CURRENCY = 'https://www.sberbank.ru/proxy/services/rates/public/history?rateType=ERNP-6&isoCodes[]=USD&date=1638997200000&regionId=038'
CLIENT_LAVEL ='PMR-4'
METALL_COD = 'A98' # Металл 98 - золото, 99 - серебро
DATA_MILLISECUND = 1638910800000
DATA_MILLISECUND = 1638997200000 # 9 декабря 2021


timestamp = 1638219600

td = datetime.datetime.fromtimestamp(timestamp)
print(f'td = {td}')
timestamp = td.timestamp()
print(f'timestamp        = {int(timestamp)}')
print(f'timestamp * 1000 = {int(timestamp*1000)}')

ctime = time.ctime(1638219600000/1000)
print(f'ctime            = {ctime}')

current_date = datetime.datetime(2021,6,21)
timedelta = datetime.timedelta(1)
today     = datetime.date.today()
end_date  = datetime.datetime(today.year, today.month, today.day)
# date_today = datetime.date.today()
while current_date <= end_date:
    print(current_date)
     # Возвращает день недели в виде целого числа, где понедельник равен 0, а воскресенье-6.
    weekday = current_date.weekday()
    if weekday <= 5:
        timestamp = int(current_date.timestamp() * 1000)
        print(f'timestamp        = {int(timestamp)}')
        
    current_date = current_date + timedelta


stop = 2
# print(text)
# print(text_json)
# print(type(metal_exchange_rates))

# save_as_readable_json(text_json)

# object_json = json.loads(text_json)
# text_json['historyRates']['1638910800000']['PMR-4']['A98']
# text_json['historyRates']['1638910800000'][CLIENT_RATING]['A98']