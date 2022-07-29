from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import requests
import random
import itertools
import time


class UserAgent:
    def get(self):
        with open("user-agents.txt") as f:
            agents_lists = f.read().split("\n")
        
        return random.choice(agents_lists)


class KalimatiMarket:
    def __init__(self, website_url):
        self.headers = {"User-Agent": UserAgent().get()}
        self.website_url = website_url

        self.req = requests.get(self.website_url, headers=self.headers)
        
        # Setting up the selenium driver. The Kalimati website is heavily rendered with Javascripts so browser automation is the way:
        opt = Options()
        path = Service("c:\\users\\chromedriver.exe")
        arguments = ['--no-sandbox', 'start-maximized', "disable-infobars", "--disable-extensions","--disable-gpu",
             '--disable-dev-shm-usage']
        opt.headless = True
        opt.add_experimental_option('excludeSwitches', ['enable-logging'])

        for arg in arguments:
            opt.add_argument(arg)

        self.driver = webdriver.Chrome(service=path, options=opt)        
        
    
    def status_code(self):
        return self.req.status_code    
    

    def daily_date(self):
        self.driver.get(self.website_url)
        
        date_xpath_selector = "//h4[@class='bottom-head']"
        WebDriverWait(self.driver, 10).until((EC.presence_of_element_located((By.XPATH, date_xpath_selector))))

        content = self.driver.page_source
        soup = BeautifulSoup(content, 'lxml')
        
        date = soup.find('h4', class_='bottom-head').text.strip().replace("""दैनिक मूल्य बारे जानकारी
- वि.सं. """, "")
        return date


    def scrape(self):       
        self.driver.get(self.website_url)
        print(f"Scraping.")
        time.sleep(2)

        # Xpath selector:
        table_xpath = "//table[@id='commodityPriceParticular']"
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, table_xpath)))
        
        content = self.driver.page_source
        soup = BeautifulSoup(content, 'lxml')
        commodity_table = soup.find('table', id='commodityPriceParticular').find('tbody')
        # The below method is List comprehension method from Python. It save lots of lines of code. Ideally you can use conventional 'for' loop and store the value in lists.
        market_lists = [[tab.find_all('td')[i].text.strip() for tab in commodity_table] for i in range(0, 5)]
        # Below lists will store all the scraped datas in tuple for databases:
        lists_of_markets = list(zip(market_lists[0], market_lists[1], market_lists[2], market_lists[3], market_lists[4]))
        
        return lists_of_markets

       
