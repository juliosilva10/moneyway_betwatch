import os
import re
import requests
from bs4 import BeautifulSoup
import time
import warnings

import re
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

from webdriver_manager.chrome import ChromeDriverManager

warnings.filterwarnings('ignore')
options = webdriver.ChromeOptions()
#
# options.add_argument('--headless')
# options.add_argument('--no-sandbox')
# options.add_argument('--disable-dev-shm-usage')

service = Service(ChromeDriverManager().install())
chrome = webdriver.Chrome(service=service)

chrome.implicitly_wait(3)
print('\n')
print('Lista de Jogos')
print('\n')

# Não detectar automação
url = 'https://betwatch.fr/money'
headers = {
    'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 \
    (KHTML, like Gecko) Chrome / 86.0.4240.198Safari / 537.36"
}

chrome.get(url)

time.sleep(5)

chrome.find_element(By.XPATH, '//*[@id="refresh-dropdown"]/option[6]').click()

time.sleep(2)

last_height = chrome.execute_script("return document.body.scrollHeight")

while True:

    # Scroll down to the bottom

    chrome.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    # Wait for page to load

    time.sleep(3)

    # Calculate new scroll height and compare with last scroll height

    new_height = chrome.execute_script("return document.body.scrollHeight")

    if new_height == last_height:

        break

    last_height = new_height


games = chrome.find_elements(By.XPATH, '/html/body/div/div/div[@class="container"]/div[@id="matchs"]/div')

for game in games:
    match_element = game.find_element(By.XPATH, '/html/body/div/div/div[@class="container"]/div[@id="matchs"]/div')
    text = match_element.text

    regex = re.compile(r"""
        (?P<time>\d{2}:\d{2})\s*
        (?P<event>[^\n]+)\s*
        (?P<teams>[^\n]+)\s*
        (?P<section1>[^\n]+)\s*
        (?P<one_value>[\d\s]+€)\s*
        (?P<one_percentage>\d+%)\s*
        (?P<one_change>[\d.]+)\s*
        (?P<sectionX>[^\n]+)\s*
        (?P<x_value>[\d\s]+€)\s*
        (?P<x_percentage>\d+%)\s*
        (?P<x_change>[\d.]+)\s*
        (?P<section2>[^\n]+)\s*
        (?P<two_value>[\d\s]+€)\s*
        (?P<two_percentage>\d+%)\s*
        (?P<two_change>[\d.]+)
        """, re.VERBOSE)

    match = regex.search(text) # Até aqui o código funciona normal, puxando os dados.

    if match:
        data = match.groupdict()

        # Organizing data in a structured format
        result = f"""
            {data['time']} | {data['event']} | {data['teams']}
            {data['section1']}: {data['one_value']} ({data['one_percentage']}) {data['one_change']}
            {data['sectionX']}: {data['x_value']} ({data['x_percentage']}) {data['x_change']}
            {data['section2']}: {data['two_value']} ({data['two_percentage']}) {data['two_change']}
            """
        print(result)
    else:
        print("Dados não encontrados")

chrome.quit()




