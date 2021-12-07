"""
Скраппинг курсов драгоценных металлог сайта sberbank.ru
"""

from urllib.parse import urlparse
# from bs4 import BeautifulSoup
import json
# import re
# import datetime
import requests
# import user_agents as ua
from fake_useragent import UserAgent

HEADERS_SBER_BANK = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:94.0) Gecko/20100101 Firefox/94.0',
}

FULL_URL = 'https://www.sberbank.ru/proxy/services/rates/public/history?rateType=PMR-4&isoCodes[]=A98&date=1638219600000&regionId=038'


def get_html(full_url, label_redirects=1):
    result = {'html':'', 'status':0}

    if label_redirects == 1:
        allow_redirects = True
    else:
        allow_redirects = False

    ua = UserAgent()
    headers = HEADERS_SBER_BANK.copy()
    headers['User-Agent'] = ua.random

    get_result = requests.get(full_url, headers=headers, allow_redirects=allow_redirects)
    result['status'] = get_result.status_code
    result['html'] = get_result.text
    result['json'] = get_result.json()

    return result

def save_as_readable_json(text):
    readable_file_path = 'readable_data.json'
    with open(readable_file_path, 'w') as f:
        json.dump(text, f, indent=4)


get_html = get_html(FULL_URL)
text_html = get_html['html']
text_json = get_html['json'] 
# print(text)
print(text_json)

save_as_readable_json(text_json)

