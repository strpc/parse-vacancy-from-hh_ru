import aiohttp
from bs4 import BeautifulSoup as BS

import asyncio
import csv
import sys
from time import time


async def get_response(url, session, name=None, page=None):
    if page != None:
        params['page'] = page
    async with session.get(url, params=params, headers=headers) as response:
        data = await response.text()
        if page == None:
            return data
        get_data(data)


def get_data(response):
    soup = BS(response, 'lxml')
    data = []
    divs = soup.find_all('div', {'data-qa': 'vacancy-serp__vacancy',
                                 'class': 'vacancy-serp-item'})
    for div in divs:
        title = div.find('a', {'data-qa': 'vacancy-serp__vacancy-title'}).text
        try:
            cost = div.find(
                # data-qa="vacancy-serp__vacancy-compensation"
                'span', {'data-qa': 'vacancy-serp__vacancy-compensation'}).text
        except:
            cost = "-"
        company = div.find(
            'div', {'class': 'vacancy-serp-item__info'}).text
        url = div.find(
            'a', {'data-qa': 'vacancy-serp__vacancy-title'}).get('href')
        discription = div.find('div', {'class': 'g-user-content'}).text
        date = div.find(
            'span', {'class': 'vacancy-serp-item__publication-date'}).text
        write_data({'date': date.strip(),
                    'title': title.strip(),
                    'cost': cost,
                    'company': company,
                    'url': url,
                    'discription': discription.strip()})


def write_data(data):
    global count
    with open('data_from_hh.csv', 'a') as file:
        order = ['date', 'title', 'cost', 'company', 'url', 'discription']
        writer = csv.DictWriter(
            file, fieldnames=order, delimiter=';',
            quoting=csv.QUOTE_NONNUMERIC)
        writer.writerow(data)
    count += 1


async def get_vacancy(name):
    url = 'https://hh.ru/search/vacancy'
    params['text'] = name

    async with aiohttp.ClientSession() as session:
        r = asyncio.create_task(get_response(url, session, name))
        html = await asyncio.gather(r)
    soup = BS(html[0].strip(), 'lxml')
    pages = soup.find_all(
        'span', {'class': 'pager-item-not-in-short-range'})[-1].find('a').get(
        'data-page')
    tasks = []

    async with aiohttp.ClientSession() as session:
        for page in range(1, int(pages)+1):
            task = asyncio.create_task(get_response(url, session, name, page))
            tasks.append(task)
        await asyncio.gather(*tasks)
    print(f'Done. {count} vacancy with title "{name}" saved.\n'
          'View file "data_from_hh.csv"')


if __name__ == '__main__':
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_0) \
            AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 \
                                        Safari/537.36', 'accept': '*/*'
               }
    params = {
        'L_is_autosearch': 'false', 'area': 1, 'clusters': 'true',
        'enable_snippets': 'true'
    }
    name = ''
    count = 0

    if len(sys.argv) > 1:
        print('We are looking for vacancy with the name:', end=" ")
        for i in sys.argv[1:]:
            if i == sys.argv[-1]:
                print(i)
                name += i
                break
            name += i + " "
            print(i, end=" ")
    else:
        name = input('Enter vacancy title: ')
    print('Please, wait')
    start_time = time()
    asyncio.run(get_vacancy(name))
    print(f"Passed {round(time() - start_time, 2)} sec")
