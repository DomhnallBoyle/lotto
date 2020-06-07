"""
    Filename: find_jackpots.py
    Description: Scrape the clubs list and find their lotto jackpots
    Author: Domhnall Boyle
    Maintained by: Domhnall Boyle
    Email: domhnallboyle@gmail.com
    Python Version: 3.6
"""
import json
import os

from driver import driver_session
from selenium.common.exceptions import NoSuchElementException

BASE_URL = 'http://klubfunder.com'
CLUB_LIST_URL = f'{BASE_URL}/Clubs/Search'


def get_club_urls():
    print('************* FINDING CLUBS *************')
    with driver_session() as driver:
        driver.get(CLUB_LIST_URL)

        page_counter = 0
        urls = []

        while True:
            print(f'Processing page: {page_counter + 1}')

            club_elements = driver.find_elements_by_class_name('stiona')
            for club_element in club_elements:
                club_link_attribute = club_element.find_element_by_tag_name('a')
                club_url = club_link_attribute.get_property('href')
                urls.append(club_url)

            try:
                # click next button if exists
                driver.find_element_by_id('nextButton').click()
            except NoSuchElementException:
                break

            page_counter += 1

        return urls


def find_jackpots(club_urls):
    print('************* FINDING JACKPOTS *************')

    with driver_session() as driver:
        results = []

        for club_url in club_urls:
            driver.get(club_url)
            try:
                table = driver.find_element_by_class_name('table')
                table_body = table.find_element_by_tag_name('tbody')
                first_row = table_body.find_element_by_tag_name('tr')
                first_rows_columns = first_row.find_elements_by_tag_name('td')
                jackpot = first_rows_columns[3].text
                currency, amount = jackpot.split(' ')
                amount = int(amount)
                if currency != '£':
                    # convert euros to pounds
                    amount *= 0.84
                print(f'{club_url}: £{amount}')
                results.append([club_url, amount])
            except NoSuchElementException:
                continue

        return results


def json_load(file_path):
    with open(file_path, 'r') as f:
        return json.load(f)


def json_dump(file_path, o):
    with open(file_path, 'w') as f:
        json.dump(o, f)


def main():
    if not os.path.exists('club_urls.json'):
        club_urls = get_club_urls()
        json_dump('club_urls.json', club_urls)
    else:
        club_urls = json_load('club_urls.json')

    if not os.path.exists('jackpots.json'):
        jackpots = find_jackpots(club_urls=club_urls)
        json_dump('jackpots.json', jackpots)
    else:
        jackpots = json_load('jackpots.json')

    jackpots.sort(key=lambda x: x[1], reverse=True)
    for jackpot in jackpots[:10]:
        print(jackpot)


if __name__ == '__main__':
    main()
