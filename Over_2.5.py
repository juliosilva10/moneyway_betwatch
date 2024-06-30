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
from tabulate import tabulate

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
    text = game.text
    #r1 = re.split(r'\s', text) # Separa as strings
    #r1 = re.split(r'\d+', text) # Remove os dígitos
    regex = re.compile(r"""
    (?P<time>\d{2}:\d{2}\s*)
    (?P<event>[^\n]+\s*)
    (?P<teams>[^\n]+\s*)
    (?P<under>[^\n]+\s*)
    (?P<under_money>[\d\s]+€\s*)
    (?P<under_percent>\d+%\s*)
    (?P<under_odd>[^\n]+\s*)
    (?P<over>[^\n]+\s*)
    (?P<over_money>[\d\s]+€\s*)
    (?P<over_percent>[\d\s]+%\s*)
    (?P<over_odd>[\d\s]+\s*)
    """, re.VERBOSE)

    match = regex.search(text)

    if match:
        data = match.groupdict()

        result = f"""
        {data['time']} {data['event']} {data['teams']} {data['under']} {data['under_money']} {data['under_percent']} {data['under_odd']}
        {data['over']} {data['over_money']} {data['over_percent']} {data['over_odd']}
        """
        #tabela = (data['time'], data['event'])

        print(result)

        #print(tabulate(tabela, headers='keys', tablefmt='pretty'))

    else:
        print("Dados não encontrados!")

chrome.quit()






    #'Time': result['time'],
    #'Event,' 'Teams', 'Under', 'Money', '%', 'Odd']

    #print(tabulate(columns, headers='keys', tablefmt="pretty"))
