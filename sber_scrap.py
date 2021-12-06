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

HEADERS_SBER_BANK = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:94.0) Gecko/20100101 Firefox/94.0',
}
HEADERS_WIKI = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36',
}

FULL_URL = 'https://www.sberbank.ru/proxy/services/rates/public/history?rateType=PMR-4&isoCodes[]=A98&date=1638219600000&regionId=038'


def get_html(full_url, label_redirects=1):
    result = {
        'html':'',
        'status':0
    }
    if label_redirects == 1:
        allow_redirects = True
    else:
        allow_redirects = False

    # full_url = 'http://en.wikipedia.org{}'.format(pageUrl)
    get_result = requests.get(full_url, headers=HEADERS_SBER_BANK, allow_redirects=allow_redirects)
    result['status'] = get_result.status_code
    html = get_result.text
    result['html'] = html
    result['json'] = get_result.json()

    return result

def save_as_readable_json(text):
    readable_file_path = 'readable_data.json'
    with open(readable_file_path, 'w') as f:
        json.dump(text, f, indent=4)


get_html = get_html(FULL_URL)
text = get_html['html']
text_json = get_html['json'] 
# print(text)
print(text_json)

save_as_readable_json(text_json)
