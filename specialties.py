import csv
import itertools
import os
import re

import requests
from bs4 import BeautifulSoup

URLS = ['https://www.alem-edu.kz/ru/university/rgp-na-phv-evrazijskij-naczionalnyj/',
        'https://www.alem-edu.kz/ru/university/astana-it-university/',
        'https://www.alem-edu.kz/ru/university/kazahskij-agrotehnicheskij-universitet-imeni-sakena-sejfullina/',
        'https://www.alem-edu.kz/ru/university/nazarbaev-universitet/',
        'https://www.alem-edu.kz/ru/university/uchrezhdenie-kazahskij-universitet-t/',
        'https://www.alem-edu.kz/ru/university/uchrezhdenie-vysshego-obrazovaniya-evr/',
        'https://www.alem-edu.kz/ru/university/universitet-kazgyuu-imeni-m-s-narikbae/',
        'https://www.alem-edu.kz/ru/university/ao-mediczinskij-universitet-astana/',
        'https://www.alem-edu.kz/ru/university/finansovaya-akademiya/',
        'https://www.alem-edu.kz/ru/university/gu-kazahskij-naczionalnyj-universi/']

URLS_EXTRA = [
    'https://univision.kz/univ/23-evraziyskiy-natsionalnyy-universitet-im-l-n-gumileva/edu-program',
    'https://univision.kz/univ/119-astana-it-university/edu-program',
    'https://univision.kz/univ/41-kazahskiy-agrotehnicheskiy-universitet-imeni-s-seyfullina/edu-program',
    None,
    'https://univision.kz/univ/53-kazahskiy-universitet-tehnologii-i-biznesa/edu-program',
    'https://univision.kz/univ/22-evraziyskiy-gumanitarnyy-institut/edu-program',
    'https://univision.kz/univ/44-universitet-kazgyuu-imeni-m-s-narikbaeva/edu-program',
    'https://univision.kz/univ/81-meditsinskiy-universitet-astana/edu-program',
    'https://univision.kz/univ/108-finansovaya-akademiya/edu-program',
    'https://univision.kz/univ/49-kazahskiy-natsionalnyy-universitet-iskusstv/edu-program'
]

HEADERS = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36',
    'accept': '*/*'}
FILE = 'specialties.csv'


def get_html(url, params=None):
    if url is None:
        return False
    else:
        r = requests.get(url, headers=HEADERS, params=params)
        return r


def specialities_parse_extra(attr_value: str, spec_list: list, category: int, university_id: int):
    html = get_html(URLS_EXTRA[university_id - 1])
    if html is False:
        return spec_list
    else:
        soup = BeautifulSoup(html.text, 'html.parser')
        items = soup.find_all('body')
        for item in items:
            try:
                specialty_items = item.find('div', class_='tab-content').find('div', class_='tab-pane', attrs={"id": attr_value}).find('div', class_='list-group').find_all('a', class_='list-group-item')
                for specialty_item in specialty_items:
                    speciality_full = specialty_item.find('div').find('h6').get_text(strip=True)
                    code = speciality_full[:7].strip()
                    name = speciality_full[7:].strip()
                    spec_list.append({
                        'code': code,
                        'name': name,
                        'category': category,
                        'university_id': university_id
                    })
            except AttributeError:
                continue

    return spec_list
    # for specialty_item in specialty_items:
    #     speciality_full = specialty_item.find('div').find('h6').get_text(strip=True)
    #     code = speciality_full[:7].strip()
    #     name = speciality_full[7:].strip()
    #     spec_list.append({
    #         'code': code,
    #         'name': name,
    #         'category': category,
    #         'university_id': university_id
    #     })
    # return spec_list


def specialties_parse(div_class: str, spec_list: list, item, category: int, university_id: int):
    try:
        specialty_items = item.find('div', class_=div_class).find('div', class_='row specialty__row').find_all('div', class_='jsspecialty__item')
        for specialty_item in specialty_items:
            specialties_full_list = specialty_item.find('div', class_='jsspecialty__item--body').find_all('div', class_='jsspecialty__line')
            for specialty_full in specialties_full_list:
                specialty_full = specialty_full.find('div', class_='jsspecialty__line--top').get_text(strip=True)
                code = specialty_full.split('-')[0].strip()
                name = specialty_full.split('-')[1].strip()
                spec_list.append({
                    'code': code,
                    'name': name,
                    'category': category,
                    'university_id': university_id
                })
            # specialties_full_list = specialty_item.find('div', class_='jsspecialty__item--body').find_all('div', class_='jsspecialty__line')
            # for specialty_full in specialties_full_list:
            #     specialty_full = specialty_full.find('div', class_='jsspecialty__line--top').get_text(strip=True)
            #     code = specialty_full.split('-')[0].strip()
            #     name = specialty_full.split('-')[1].strip()
            #     spec_list.append({
            #         'code': code,
            #         'name': name,
            #         'category': category,
            #         'university_id': university_id
            #     })
    except AttributeError:
        spec_list.append({
            'code': '-',
            'name': 'Не имеется информации',
            'category': category,
            'university_id': university_id
        })

    return spec_list


def get_content(html, university_id):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('body')
    specialties_list = []
    for item in items:
        specialties_list = specialties_parse('news__tab--item js__tab--item js__tab--bakalav', specialties_list, item, 1, university_id)
        # specialties_list = specialities_parse_extra('ep_1', specialties_list, 1, university_id)
        specialties_list = specialties_parse('news__tab--item js__tab--item js__tab--magistr', specialties_list, item, 2, university_id)
        specialties_list = specialities_parse_extra('ep_2', specialties_list, 2, university_id)
        specialties_list = specialties_parse('news__tab--item js__tab--item js__tab--doct', specialties_list, item, 3, university_id)
        specialties_list = specialities_parse_extra('ep_6', specialties_list, 3, university_id)
    #     specialty_items_bakalavr = item.find('div', class_='news__tab--item js__tab--item js__tab--bakalav').find('div', class_='row specialty__row').find_all('div', class_='jsspecialty__item')
    #     for specialty_item_bakalavr in specialty_items_bakalavr:
    #         specialties_full_list = specialty_item_bakalavr.find('div', class_='jsspecialty__item--body').find_all('div', class_='jsspecialty__line')
    #         for specialty_full in specialties_full_list:
    #             specialty_full = specialty_full.find('div', class_='jsspecialty__line--top').get_text(strip=True)
    #             code = specialty_full.split('-')[0].strip()
    #             name = specialty_full.split('-')[1].strip()
    #             specialties_list.append({
    #                 'code': code,
    #                 'name': name,
    #                 'category': 1,
    #                 'university_id': university_id
    #             })

        # filter by code then by name
        check_code = []
        check_name = []
        result_by_code = []
        result_by_name = []
        for spec in specialties_list:
            if spec['code'] not in check_code:
                result_by_code.append(spec)
                check_code.append(spec['code'])
        for spec in result_by_code:
            if spec['name'] not in check_name:
                result_by_name.append(spec)
                check_name.append(spec['name'])
    return result_by_name


def save_file(items, path):
    with open(path, 'w', newline='', encoding='utf-8-sig') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow([
            'id',
            'code',
            'name',
            'category',
            'university_id',
        ])
        for index, item in enumerate(items, start=1):
            writer.writerow([
                index,
                item['code'],
                item['name'],
                item['category'],
                item['university_id']
            ])


specialties = []


def parse(urls):
    print('---------------------------------------------')
    i = 1
    for url in urls:
        print(f'Выполнение парсинга специальностей: {i} из {len(urls)}...')
        html = get_html(url)
        if html.status_code == 200:
            specialties.extend(get_content(html.text, i))
            i = i + 1
        else:
            print('Error')
    print('---------------------------------------------')
    return specialties


parse(URLS)
print(f'Получено {len(specialties)} специальностей')
save_file(specialties, FILE)
os.startfile('specialties.csv')
