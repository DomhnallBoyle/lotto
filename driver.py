"""
    Filename: 
    Description:
    Author: Domhnall Boyle
    Maintained by: Domhnall Boyle
    Email: domhnallboyle@gmail.com
    Python Version: 3.6
"""
from contextlib import contextmanager

from selenium import webdriver
from selenium.webdriver.chrome.options import Options


@contextmanager
def driver_session():
    chrome_options = Options()
    chrome_options.add_argument('--headless')

    driver = webdriver.Chrome('./chromedriver', chrome_options=chrome_options)
    yield driver
    driver.close()
