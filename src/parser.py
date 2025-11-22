from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import traceback

from models import Perfume
from utils import scroll_to_bottom, clean_html_text
from config import USER_AGENT, START_URL, SCROLL_PAUSE, BASE_URL

class PerfumeParser:
    def __init__(self, scrolls=None):
        chrome_options = Options()
        chrome_options.add_argument(f"user-agent={USER_AGENT}")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        self.browser = webdriver.Chrome(service=Service(), options=chrome_options)
        self.scrolls = scrolls
        self.products = []

    def close(self):
        self.browser.quit()

    def open_page(self, url):
        self.browser.get(url)
        time.sleep(5)
        self.handle_location()
        self.handle_modal()

    def handle_location(self):
        try:
            aside = WebDriverWait(self.browser, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".ga-header__location-confirm-address"))
            )
            aside.find_element(By.CSS_SELECTOR, "button:nth-child(2)").click()
            time.sleep(2)
        except Exception:
            pass

    def handle_modal(self):
        try:
            close_button = WebDriverWait(self.browser, 5).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'aside button[data-transaction-name="ga-modal-close-button"]'))
            )
            close_button.click()
        except Exception:
            pass

    def parse_products(self):
        print("Скроллим страницу...")
        scroll_to_bottom(self.browser, pause_time=SCROLL_PAUSE, max_scrolls=self.scrolls)
        print("Скролл завершен")

        articles = self.browser.find_elements(By.CSS_SELECTOR, "article")
        print(f"Найдено товаров: {len(articles)}")

        for i, article in enumerate(articles):
            print(f"Парсинг товара {i+1}/{len(articles)}")
            try:
                perfume = self.parse_article(article)
                self.products.append(perfume)
            except Exception as e:
                print("Ошибка при парсинге карточки:", e)
                traceback.print_exc()

    def parse_article(self, article):
        # Ссылка
        link_el = article.find_element(By.CSS_SELECTOR, "a")
        href = link_el.get_attribute("href")
        link = href if href.startswith("http") else BASE_URL + href

        # Бренд и название
        try:
            brand_block = article.find_element(By.CSS_SELECTOR, '[itemtype="https://schema.org/Brand"]')
            brand = brand_block.find_element(By.CSS_SELECTOR, 'meta[itemprop="name"]').get_attribute("content")
            try:
                name = article.find_element(
                    By.XPATH,
                    './/meta[@itemprop="name" and not(ancestor::*[@itemtype="https://schema.org/Brand"])]'
                ).get_attribute("content")
            except:
                pass
        except:
            brand = None
            name = None

        # Цена
        try:
            price = article.find_element(By.CSS_SELECTOR, "meta[itemprop='price']").get_attribute("content")
        except:
            price = None

        # Рейтинг
        try:
            rating = article.find_element(By.CSS_SELECTOR, "meta[itemprop='ratingValue']").get_attribute("content")
        except:
            rating = None

        # Внутренняя карточка
        self.browser.execute_script("window.open(arguments[0], '_blank');", link)
        self.browser.switch_to.window(self.browser.window_handles[-1])
        time.sleep(5)

        # Описание
        try:
            desc_div = self.browser.find_element(By.CSS_SELECTOR, "div[itemprop='description']")
            paragraphs = desc_div.find_elements(By.TAG_NAME, "p")
            if paragraphs:
                description = "\n".join(p.text.strip() for p in paragraphs if p.text.strip())
            else:
                html = desc_div.get_attribute("innerHTML")
                description = clean_html_text(html)
        except:
            description = None

        # Применение
        try:
            wrapper = self.browser.find_element(By.XPATH, "//div[@text='Применение']")
            instruction_divs = wrapper.find_elements(By.XPATH, "./div")
            instruction = "\n".join(div.get_attribute("textContent").strip() for div in instruction_divs if div.get_attribute("textContent"))
        except:
            instruction = None

        # Доп. информация
        try:
            info_div = self.browser.find_element(By.XPATH, "//div[@text='Дополнительная информация']//div")
            parts = [p.strip().lower() for p in info_div.get_attribute("innerHTML").split("<br>") if p.strip()]
            country = None
            for idx, part in enumerate(parts):
                if "страна происхождения" in part and idx+1 < len(parts):
                    country = parts[idx+1].capitalize()
                    break
        except:
            country = None

        self.browser.close()
        self.browser.switch_to.window(self.browser.window_handles[0])

        return Perfume(
            url=link, brand=brand, name=name, price=price, rating=rating,
            description=description, instruction=instruction, country=country
        )
