import datetime
import time

# td = datetime.datetime.today()
# print(f"td{td}")

timestamp = 1638219600

td = datetime.datetime.fromtimestamp(timestamp)
print(f'td = {td}')
timestamp = td.timestamp()
print(f'timestamp        = {int(timestamp)}')
print(f'timestamp * 1000 = {int(timestamp*1000)}')

ctime = time.ctime(1638219600000/1000)
print(f'ctime            = {ctime}')

current_date = datetime.datetime(2021,6,21)
delta_day = datetime.timedelta(1)
today     = datetime.date.today()
end_date  = datetime.datetime(today.year, today.month, today.day)
# date_today = datetime.date.today()
while current_date <= end_date:
    print(current_date)
    current_date = current_date + delta_day
    timestamp = current_date.timestamp()
    print(f'timestamp        = {int(timestamp)}')
