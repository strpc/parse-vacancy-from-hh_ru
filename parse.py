import requests
from bs4 import BeautifulSoup as BS

import csv
from datetime import datetime
import time
import sys


def get_response(url, name=None, page=None):
    header = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_0) \
                AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 \
                                            Safari/537.36', 'accept': '*/*'
    }
    params = {
        'L_is_autosearch': 'false', 'area': 1, 'clusters': 'true',
        'enable_snippets': 'true', 'text': name, 'page': page
    }
    r = requests.get(url, headers=header, params=params)
    return r.text


def get_data(response):
    soup = BS(response, 'lxml')
    data = []
    divs = soup.find_all('div', {'data-qa': 'vacancy-serp__vacancy', 
                                 'class': 'vacancy-serp-item'})
    for div in divs:
        title = div.find('a', {'data-qa': 'vacancy-serp__vacancy-title'}).text
        try:
            cost = div.find(
                'div', {'data-qa': 'vacancy-serp__vacancy-compensation'}).text
        except:
            cost = "-"
        company = div.find(
            'div', {'class': 'vacancy-serp-item__info'}).text
        url = div.find(
            'a', {'data-qa': 'vacancy-serp__vacancy-title'}).get('href')
        discription = div.find('div', {'class': 'g-user-content'}).text.strip()
        write_data({'title': title.strip(),
                    'cost': cost,
                    'company': company,
                    'url': url,
                    'discription': discription})


def write_data(data):
    with open('data_from_hh.csv', 'a') as file:
        order = ['title', 'cost', 'company', 'url', 'discription']
        writer = csv.DictWriter(
            file, fieldnames=order, delimiter=';', 
                    quoting=csv.QUOTE_NONNUMERIC)
        writer.writerow(data)


def get_vacancy(name):
    url = 'https://hh.ru/search/vacancy'
    soup = BS(get_response(url, name), 'lxml')
    pages = soup.find_all(
        'span', {'class': 'pager-item-not-in-short-range'})[-1].find('a'
                                                        ).get('data-page')
    for page in range(1, int(pages)+1):
        get_data(get_response(url, name, page))
        print('Data saved from %s pages' % page)
    print('Done. View file "data_from_hh.csv"')


if __name__ == '__main__':
    start_time = datetime.now()
    name = ''
    if len(sys.argv) > 1:
        print('We are looking for vacancy with the name:', end=" ")
        for i in sys.argv[1:]:
            if i == sys.argv[-1]:
                print(i)
                name += i
                break
            name += i + " "
            print(i, end=" ")
        get_vacancy(name)
    else:
        name = input('Enter vacancy title: ')
        get_vacancy(name)
    print("Passed " + str(datetime.now() - start_time))
    
