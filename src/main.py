from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json

chrome_options = Options()

user_agent = ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36')
chrome_options.add_argument(f"user-agent={user_agent}")
chrome_options.add_argument("--disable-blink-features=AutomationControlled")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

service = Service()

browser = webdriver.Chrome(service=service, options=chrome_options)

try:
    url = "https://goldapple.ru/parfjumerija"
    browser.get(url)
    time.sleep(1000)

    aside = browser.find_element(By.CSS_SELECTOR, '.ga-header__location-confirm-address')
    button_loc = aside.find_element(By.CSS_SELECTOR, 'button:nth-child(2)')
    button_loc.click()
    time.sleep(3)
    close_button = browser.find_element(By.CSS_SELECTOR, 'aside button[data-transaction-name="ga-modal-close-button]')
    close_button.click()
    time.sleep(10000)

except Exception:
    pass