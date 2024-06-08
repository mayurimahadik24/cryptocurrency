# scraper/tasks.py

from celery import shared_task
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import json

class CoinMarketCap:
    def __init__(self):
        self.service = Service(ChromeDriverManager().install())
        self.options = webdriver.ChromeOptions()
        self.options.add_argument('--headless')
        self.driver = webdriver.Chrome(service=self.service, options=self.options)
    
    def get_coin_data(self, coin):
        url = f'https://coinmarketcap.com/currencies/duko/ {coin.lower()}/'
        self.driver.get(url)
        
        data = {}
        
        try:
            data['price'] = self.driver.find_element(By.CSS_SELECTOR, '.priceValue').text
            data['price_change'] = self.driver.find_element(By.CSS_SELECTOR, '.sc-15yy2pl-0.kAXKAX span').text
            data['market_cap'] = self.driver.find_element(By.CSS_SELECTOR, '.statsValue').text
            data['volume'] = self.driver.find_element(By.XPATH, '//*[contains(text(),"Volume")]/../following-sibling::div').text
            data['circulating_supply'] = self.driver.find_element(By.XPATH, '//*[contains(text(),"Circulating Supply")]/../following-sibling::div').text
        except Exception as e:
            data['error'] = str(e)
        
        return data

    def close(self):
        self.driver.quit()

@shared_task
def fetch_crypto_data(crypto_list):
    scraper = CoinMarketCap()
    results = {}

    for crypto in crypto_list:
        results[crypto] = scraper.get_coin_data(crypto)
    
    scraper.close()
    return results

