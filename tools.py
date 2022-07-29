from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError
from bs4 import BeautifulSoup
import requests
import random
import os
import itertools
import time
import sys
import asyncio


class UserAgent:
    def get(self):
        with open("user-agents.txt") as f:
            agents_lists = f.read().split("\n")
        
        return random.choice(agents_lists)


class KalimatiMarket:
    def __init__(self):        
        self.website_url = "https://kalimatimarket.gov.np/price" 
        self.req = requests.get(self.website_url, headers={"User-Agent": UserAgent().get()})         
                
    
    def status_code(self):
        return self.req.status_code    
    

    def daily_date(self):
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True, slow_mo=1*10000)
            page = browser.new_page(user_agent=UserAgent().get())            
            page.goto(self.website_url)
        
            date_xpath_selector = "//h4[@class='bottom-head']"

            page.wait_for_selector(date_xpath_selector, timeout=1*10000)

            content = page.content()
            soup = BeautifulSoup(content, 'lxml')

            date = soup.find('h4', class_='bottom-head').text.strip().replace("""दैनिक मूल्य बारे जानकारी
                                                                              - वि.सं. """, "")
            return date

    
    def scrape(self):            
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True, slow_mo=1*10000)
            page = browser.new_page(user_agent=UserAgent().get())
            print("Scraping.")
            page.goto(self.website_url)
            
            # Xpath selector:
            table_xpath = "//table[@id='commodityPriceParticular']"
            page.wait_for_selector(table_xpath, timeout=1*10000)

            content = page.content()
            soup = BeautifulSoup(content, 'lxml')

            commodity_table = soup.find('table', id='commodityPriceParticular').find('tbody')
            
            try:
                market_lists = [[tab.find_all('td')[i].text.strip() for tab in commodity_table] for i in range(0, 5)]
            except IndexError:
                print("No data available! Try again tomorrow.")
                market_lists = ["No data available! Try again tomorrow."] * 5

            browser.close()
            return market_lists

