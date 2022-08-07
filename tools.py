from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError
from bs4 import BeautifulSoup
import requests
import random
import itertools
import time
import datetime
import re


time_now = datetime.datetime.now().strftime("%Y-%m-%d")


class UserAgent:
    def get(self):
        with open("user-agents.txt") as f:
            agents_lists = f.read().split("\n")
        
        return random.choice(agents_lists)


class KalimatiMarket:
    def __init__(self):        
        self.website_url = "https://kalimatimarket.gov.np/" 
        self.req = requests.get(self.website_url, headers={"User-Agent": UserAgent().get()})         
                
    
    def status_code(self):
        return self.req.status_code    
    

    def daily_date(self):
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True, slow_mo=1*10000)
            page = browser.new_page(user_agent=UserAgent().get())            
            page.goto(self.website_url)
        
            date_xpath_selector = "//h5[@style='padding-top:0;color:#006400']"
            page.wait_for_selector(date_xpath_selector, timeout=1*10000)

            content = page.content()
            soup = BeautifulSoup(content, 'lxml')
            date = soup.find('div', class_='features-inner even bg-white').find('h5').text.strip()                 

            browser.close()

            return date

    
    def scrape(self):            
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True, slow_mo=1*10000)
            page = browser.new_page(user_agent=UserAgent().get())
            print("Scraping.")
            page.goto(self.website_url)
            
            # Xpath selector:
            table_xpath = "//table[@id='commodityDailyPrice']"
            page.wait_for_selector(table_xpath, timeout=1*10000)

            content = page.content()
            soup = BeautifulSoup(content, 'lxml')

            commodity_table = soup.find('table', id='commodityDailyPrice').find('tbody')

            # Extracting all the market values by looping in list compreheinsion method:
            try:
              market_lists = [[tab.find_all('td')[i].text.strip() for tab in commodity_table] for i in range(0, 4)]
            except IndexError:
              print("No data available! Try again tomorrow.")
              market_lists = ["No data available! Try again tomorrow."] * 5            
            
            # Datetime of extraction in a lists:
            date_lists = [time_now] * len(market_lists[0]) 

            units = []
            commodities = []

            # Extracting only unit from commodity for separate column:
            for commodity in market_lists[0]:
                # splitting the string with special brackets and filtering out the commodity and unit values separately:
                split_strings = re.split(r"[()]", commodity)
                fresh_commos = " ".join(split_strings[:-2])

                commodities.append(fresh_commos)               # Fresh commodities
                units.append(split_strings[-2])             # Fresh units
           
            browser.close()

            # Zipping all the scraped datas in tuple for MYSQL database.
            return list(zip(date_lists, commodities, units, market_lists[1], market_lists[2], market_lists[3]))
            
