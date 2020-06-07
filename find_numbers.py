"""
    Filename: find_numbers.py
    Description: Scrape lotto numbers from a club
    Author: Domhnall Boyle
    Maintained by: Domhnall Boyle
    Email: domhnallboyle@gmail.com
    Python Version: 3.6
"""
import argparse
import json
import re
import time

from driver import driver_session
from selenium.common.exceptions import ElementNotInteractableException, NoSuchElementException

REGEX = r'The lotto results for [0-9+\/]+ are: [0-9,+]+'


def scrape_numbers(club_url):
    with driver_session() as driver:
        # find numbers on homepage
        driver.get(club_url)

        table = driver.find_element_by_class_name('table')
        table_body = table.find_element_by_tag_name('tbody')
        table_rows = table_body.find_elements_by_tag_name('tr')

        lotto_numbers = []
        for row in table_rows:
            numbers = row.find_elements_by_tag_name('td')[1].text
            numbers = [int(num) for num in numbers.split(',')]
            lotto_numbers.append(numbers)

        # find numbers on news
        club_name = club_url.split('/')[-1]
        club_news_url = f'{club_url}/news/{club_name}'
        driver.get(club_news_url)

        while True:
            time.sleep(2)
            rows = driver.find_elements_by_class_name('col-md-10')
            for row in rows:
                description = row.find_element_by_tag_name('p').text
                if re.match(REGEX, description):
                    numbers = description.split(':')[1].strip()
                    numbers = [int(num) for num in numbers.split(',')]
                    lotto_numbers.append(numbers)

            try:
                # click next button
                driver.find_element_by_class_name('next').click()
            except (NoSuchElementException, ElementNotInteractableException):
                break

        with open(f'{club_name}.json', 'w') as f:
            json.dump(lotto_numbers, f)

        return lotto_numbers


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('club_url', type=str)

    args = parser.parse_args()

    lotto_numbers = scrape_numbers(args.club_url)
    print(lotto_numbers)
