import csv
import os
import re

import requests
from bs4 import BeautifulSoup

URLS = ['https://www.alem-edu.kz/ru/university/rgp-na-phv-evrazijskij-naczionalnyj/',
        'https://www.alem-edu.kz/ru/university/astana-it-university/']
HEADERS = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36',
    'accept': '*/*'}
FILE = 'universities.csv'


def get_html(url, params=None):
    r = requests.get(url, headers=HEADERS, params=params)
    return r


def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('body')

    universities_list = []
    for item in items:
        title = item.find('div', class_='university__info--title').get_text(strip=True)
        link = item.find_all('div', class_='uni-contact__left--email')[0].find('a').get('href').strip()
        price = item.find_all('div', class_='institutions__info--price-block')[0].get_text(strip=True)
        if re.search('[0-9]', price):
            price = price
            price = re.findall(r'\d+', price)
            price = ' '.join(price)
        else:
            price = 'Цену уточняйте'
        universities_list.append({
            'title': title,
            'link': link,
            'price': price
        })
    return universities_list


def save_file(items, path):
    with open(path, 'w', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(
            ['Наименование', 'Ссылка', 'Цена за год обучения'])
        for item in items:
            writer.writerow([item['title'], item['link'], item['price']])


universities = []


def parse(urls):
    for url in urls:
        print(url)
        html = get_html(url)
        if html.status_code == 200:
            universities.extend(get_content(html.text))
        else:
            print('Error')
    return universities


parse(URLS)
print(f'Получено {len(universities)} университетов')
save_file(universities, FILE)
os.startfile('universities.csv')
