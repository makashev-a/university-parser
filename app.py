# import requests
# from bs4 import BeautifulSoup
# import pandas as pd
#
#
# def parse_info(info):
#     parse_res = pd.DataFrame()
#
#     link_univer = ''
#     price_univer = ''
#     title_univer = ''
#
#     link_univer = info.find('div', {'class': 'institutions__info--title'}).find('a').get('href').strip()
#     price_univer = info.find('div', {'class': 'institutions__info--price'}).text
#     title_univer = info.find('div', {'class': 'institutions__info--title'}).text
#
#     parse_res = parse_res.append(pd.DataFrame([[link_univer, price_univer, title_univer]],
#                                               columns=['link_univer', 'price_univer', 'title_univer']),
#                                  ignore_index=True)
#
#     return parse_res
#
#
# url = f'https://www.alem-edu.kz/ru/universitys/uchebnyye-zavedeniya/vyssheye-obrazovaniye/?%D0%B3%D0%BE%D1%80%D0%BE%D0%B4=%D0%9D%D1%83%D1%80-%D0%A1%D1%83%D0%BB%D1%82%D0%B0%D0%BD&%D1%84%D0%BE%D1%80%D0%BC%D0%B0=0&speczializacziya=0&voennaya_kafedra=0&nalichie_obshhezhitiya=0&aurl=%2Funiversitys%2Fuchebnyye-zavedeniya%2Fvyssheye-obrazovaniye%2F&aformat=institutions'
#
#
# def parsing_url(urls):
#     result = pd.DataFrame()
#
#     r = requests.get(urls)
#     soup = BeautifulSoup(r.text, features='html.parser')
#     univers = soup.find_all('div', {'class': 'institutions__item--info'})
#
#     for item in univers:
#         res = parse_info(item)
#         result = result.append(res, ignore_index=True)
#
#     result.to_excel('result.xlsx')
#
#
# parsing_url(url)

import re

import requests
from bs4 import BeautifulSoup
import csv
import os

URL = 'https://www.alem-edu.kz/ru/universitys/uchebnyye-zavedeniya/vyssheye-obrazovaniye/'
PAYLOAD = {
    'город': 'Нур-Султан',
    'форма': 0,
    'speczializacziya': 0,
    'voennaya_kafedra': 0,
    'nalichie_obshhezhitiya': 0
}
HEADERS = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36',
    'accept': '*/*'}
FILE = 'universities.csv'


def get_html(url, params=None):
    r = requests.get(url, headers=HEADERS, params=params)
    return r


def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_='institutions__item--info')

    universities = []
    for item in items:
        price = item.find('div', class_='institutions__info--price').text.replace('\t', '').replace('\n', '')
        if re.search('[0-9]', price):
            price = price
        else:
            price = 'Неизвестно'
        universities.append({
            'title': item.find('div', class_='institutions__info--title').find('a').get_text(strip=True),
            'link': item.find('div', class_='institutions__info--title').find('a').get('href').strip(),
            'price': price,
            'specialties': item.find('div', class_='institutions__specialtie--item').get_text().replace('\t',
                                                                                                        '').replace(
                '\n', ''),
            'faculties': item.find_all('div', class_='institutions__specialtie--item')[1].get_text().replace('\t',
                                                                                                             '').replace(
                '\n', '')
        })
    return universities


def save_file(items, path):
    with open(path, 'w', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(
            ['Наименование', 'Ссылка', 'Цена за год обучения', 'Кол-во специальностей', 'Кол-во факультетов'])
        for item in items:
            writer.writerow([item['title'], item['link'], item['price'], item['specialties'], item['faculties']])


def parse():
    html = get_html(URL, params=PAYLOAD)
    if html.status_code == 200:
        universities = []
        page_count = 3
        for page in range(1, page_count + 1):
            html = get_html(URL + f'/page/{page}/', params=PAYLOAD)
            universities.extend(get_content(html.text))
        save_file(universities, FILE)
        print(f'Получено {len(universities)} университетов')
        os.startfile(FILE)
    else:
        print('Error')


parse()
