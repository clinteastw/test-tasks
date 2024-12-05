import asyncio
import csv

import aiohttp
from bs4 import BeautifulSoup


def write_to_csv(animals_dict: dict):
    with open('animals.csv', 'w', encoding='utf-8') as f:
        writer = csv.writer(f)
        for k, v in animals_dict.items():
            row = [k, v]
            writer.writerow(row)


async def get_page(session: aiohttp.ClientSession, url: str) -> str:
    async with session.get(url) as resp:
        return await resp.text()


def get_next_page_link(soup):
    nav = soup.find('div', id='mw-pages')
    if nav:
        next_link = nav.find('a', string='Следующая страница')
        if next_link:
            return next_link['href'].replace(" ", "_")
    return None


async def count_animals_by_letter_on_page(html: str, animals_count: dict):
    soup = BeautifulSoup(html, 'lxml')
    div = soup.find('div', attrs={'class': 'mw-category mw-category-columns'})
    if div:
        uls = div.find_all('ul')
        for ul in uls:
            links = ul.find_all('a')
            for link in links:
                text = link.text.strip()
                first_letter = text[0]
                if first_letter not in animals_count:
                    animals_count[first_letter] = 1
                else:
                    animals_count[first_letter] += 1


async def main() -> dict:
    start_url = 'https://ru.wikipedia.org/wiki/Категория:Животные_по_алфавиту'
    animals_count = {}
    
    async with aiohttp.ClientSession() as session:
        current_url = start_url
        tasks = []
        
        while True:
            html = await get_page(session, current_url)
            task = asyncio.create_task(
                count_animals_by_letter_on_page(html, animals_count)
            )
            tasks.append(task)
            next_page_url = get_next_page_link(BeautifulSoup(html, 'lxml'))
            if not next_page_url:
                break
            current_url = f'https://ru.wikipedia.org{next_page_url}'

        await asyncio.gather(*tasks)

    write_to_csv(animals_count)
    return animals_count


if __name__ == '__main__':
    print('Собираю данные')
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(main())
