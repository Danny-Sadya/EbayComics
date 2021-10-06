import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver import ChromeOptions
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
import os
import sqlite3
import sys
from cgcValueScraper import get_values_and_grades
import re
import requests
import cv2
import difflib
import random
from selenium.webdriver.common.by import By


class EbayScraper:
    scraped_items = []
    matched_items = []

    def __init__(self):
        self.product_title = "avengers #2"
        self.search_query = self.product_title + ' cgc'
        self.min_grade = 0.0
        self.price_percentage = 100
        self.floor_price = 85
        self.max_grade = 10.0
        self.negative_words = ''
        self.cgc_link = 'https://comics.gocollect.com/guide/view/124346'

        # self.product_title = sys.argv[1]
        # self.search_query = self.product_title + ' cgc'
        # self.cgc_link = sys.argv[2]
        # self.price_percentage = int(sys.argv[3])
        # self.floor_price = int(sys.argv[4])
        # self.min_grade = float(sys.argv[5])
        # self.max_grade = float(sys.argv[6])
        # self.negative_words = str(sys.argv[7])

        self.grades_values, self.img_url = get_values_and_grades(self.cgc_link)
        self.get_comics_image()
        options = ChromeOptions()
        options.add_argument("--start-maximized")
        # options.add_argument("--headless")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        options.add_argument("--disable-blink-features=AutomationControlled")
        self.driver = webdriver.Chrome(executable_path=os.path.abspath(os.getcwd()) + r"\chromedriver.exe",
                                       options=options)
        self.driver.set_page_load_timeout(30)

    def open_ebay_and_start_scraping(self):
        try:
            self.driver.get('https://www.ebay.com/sch/ebayadvsearch?_ul=BY')
            time.sleep(5)
            self.find_a_product()

            time.sleep(5)
            i = 1
            while True:
                print(f'page #{i}')
                i += 1
                self.scroll_page()
                self.scrape_items()
                is_next_page = self.move_to_the_next_page()
                if not is_next_page:
                    break

            self.scraped_items = [dict(t) for t in {tuple(d.items()) for d in self.scraped_items}]
            self.find_items_that_fit_criterias()

            print(len(self.scraped_items))
            print(self.matched_items)
            print(len(self.matched_items))
        except Exception as ex:
            print('Runtime error: ', ex)
        finally:
            time.sleep(5)
            self.delete_comics_image()
            self.driver.close()
            self.driver.quit()

    def find_items_that_fit_criterias(self):
        for item in self.scraped_items:
            if self.match_comics_name(item):
                if self.is_cgc_in_title(item):
                    grade = self.find_grade_in_title(item)
                    if grade:
                        if self.match_grade_criteria(grade) and self.match_price_criteria(item, grade):
                            if self.compare_photos(item):
                                self.matched_items.append(item)

    def match_comics_name(self, item):
        try:
            splited_title = self.product_title.split("#")
            match = re.search(r'{}\b'.format(self.product_title.lower()), item['title'].lower())
            match = re.search(r'{}[ #%]{}\b'.format(splited_title[0].lower().strip(), splited_title[1]), item['title'].lower())
            if match:
                return True
            else:
                return False
        except Exception as ex:
            print('Cannot match comics name: ', ex)
            return False

    def match_price_criteria(self, item, grade):
        try:
            cgc_cost = list(x for x in self.grades_values if x[0] == grade)[0][1]
            cost_that_user_willing_to_pay = (100 + self.price_percentage) * cgc_cost / 100
            floor_cost = (100 - self.floor_price) * cgc_cost / 100
            if floor_cost <= item['cost'] <= cost_that_user_willing_to_pay:
                return True
            return False
        except Exception as ex:
            print('Cannot match price criterias: ', ex)
            print(grade, item)
            return False

    def match_grade_criteria(self, grade):
        try:
            if self.min_grade <= grade <= self.max_grade:
                return True
            return False
        except Exception as ex:
            print('Cannot match grade criterias: ', ex)
            return False

    def is_cgc_in_title(self, item):
        try:
            if 'cgc' in item['title'].lower():
                return True
            return False
        except Exception as ex:
            print('Cannot find cgc in title: ', ex)
            return False

    def find_grade_in_title(self, item):
        try:
            match = re.search(r'cgc \d[.,]\d', item['title'].lower()) or re.search(r'\d[.,]\d cgc', item['title'].lower())
            if match:
                grade = match[0].split(' ')[1].replace(',', '.')
                return float(grade)
            return None
        except Exception as ex:
            print('Cannot find grade in title: ', ex)
            return None

    def find_a_product(self):
        try:
            searchquery_button = self.driver.find_element_by_xpath("//input[@name='_nkw']")
            searchquery_button.click()
            searchquery_button.send_keys(self.search_query)
            negative_keywords_button = self.driver.find_element_by_xpath("//input[@name='_ex_kw']")
            negative_keywords_button.click()
            negative_keywords_button.send_keys(self.negative_words)
            select_items_per_page_button = Select(self.driver.find_element_by_xpath("//select[@name='_ipg']"))
            select_items_per_page_button.select_by_value('200')
            search_button = self.driver.find_element_by_xpath("//button[@id='searchBtnLowerLnk']")
            search_button.click()

        except Exception as ex:
            print('Error in product finding: ', ex)

    def scrape_items(self):
        try:
            soup = self.create_soup()
            soup = soup.find('div', class_='left-center').find('ul', id='ListViewInner')
            cards = soup.find_all('li', class_='sresult lvresult clearfix li')
            cards.extend(soup.find_all('li', class_='sresult lvresult clearfix li shic'))

            for card in cards:
                try:
                    title = card.find('div', class_='lvpic pic img left').find('div', class_='lvpicinner full-width picW').find(
                        'img').get('alt')
                    cost = float(
                        card.find('ul', class_='lvprices left space-zero').find('span', class_='bold')
                            .text.replace('\xa0', '').replace(
                            '\n', '').replace('US $', '').replace(',', '.').strip().split(' ')[-1])
                    url = card.find('h3', class_='lvtitle').find('a', class_='vip').get('href')

                    img_url = card.find('div', class_='lvpic pic img left').find('div', class_='lvpicinner full-width picW').find(
                        'img').get('src')

                    bid = card.find('ul', class_='lvprices left space-zero').find('li', class_='lvformat').text
                    bid_format = "Auction" if 'став' in bid or 'bid' in bid  else "Buy it now"

                    self.scraped_items.append({
                        "title": title,
                        "cost": cost,
                        'bid_format': bid_format,
                        'url': url,
                        "img_url": img_url
                    })
                except Exception as ex:
                    print(title, ex)

        except Exception as ex:
            print('Error in cards scraping: ', ex)

    def move_to_the_next_page(self):
        try:
            current_url = self.driver.current_url
            button = self.driver.find_element_by_xpath("//a[@class='gspr next']")
            if button.get_attribute('href') == current_url:
                return False
            button.click()
            return True
        except Exception:
            try:
                splited = self.driver.current_url.split("&")
                for i in range(0, len(splited)):
                    if splited[i].startswith('_pgn'):
                        splitted_page = splited[i].split('=')
                        splitted_page[1] = str(int(splitted_page[1]) + 1)
                        splited[i] = "=".join(splitted_page)

                        splitted_item_count = splited[i + 1].split('=')
                        splitted_item_count[1] = str(int(splitted_item_count[1]) + 200)
                        splited[i + 1] = "=".join(splitted_item_count)
                        break
                next_url = "&".join(splited)
                self.driver.get(next_url)
                button = self.driver.find_element_by_xpath("//a[@class='gspr next']")
                if button.get_attribute('href') == self.driver.current_url:
                    return False
                return True

            except Exception as ex:
                return False

    def scroll_page(self):
        try:
            SCROLL_PAUSE_TIME = 0.5

            last_height = self.driver.execute_script("return document.body.scrollHeight")
            # Get scroll height

            while True:
                # Scroll down to bottom
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

                # Wait to load page
                time.sleep(SCROLL_PAUSE_TIME)

                # Calculate new scroll height and compare with last scroll height
                new_height = self.driver.execute_script("return document.body.scrollHeight")
                if new_height == last_height:
                    break
                last_height = new_height
        except Exception as ex:
            print('Error while scrolling: ', ex)

    def create_soup(self):
        return BeautifulSoup(self.driver.page_source, 'lxml')

    def get_comics_image(self):
        r = requests.get(self.img_url)
        with open(f'photo_temp/{self.product_title}.jpg', 'wb') as f:
            f.write(r.content)

    def delete_comics_image(self):
        os.remove(f'photo_temp/{self.product_title}.jpg')

    def CalcImageHash(self, FileName):
        image = cv2.imread(FileName)
        resized = cv2.resize(image, (8, 8), interpolation=cv2.INTER_AREA)
        gray_image = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
        avg = gray_image.mean()  # Среднее значение пикселя
        ret, threshold_image = cv2.threshold(gray_image, avg, 255, 0)  # Бинаризация по порогу

        # Рассчитаем хэш
        _hash = ""
        for x in range(8):
            for y in range(8):
                val = threshold_image[x, y]
                if val == 255:
                    _hash = _hash + "1"
                else:
                    _hash = _hash + "0"

        return _hash

    def compareHash(self, hash1, hash2):
        l = len(hash1)
        i = 0
        count = 0
        while i < l:
            if hash1[i] != hash2[i]:
                count = count + 1
            i = i + 1
        return count

    def compare_photos(self, item):
        try:
            r = requests.get(item['img_url'])
            suffix = random.randint(10000, 100000)
            with open(f'photo_temp/{self.product_title}_{suffix}.jpg', 'wb') as f:
                f.write(r.content)
                hash1 = self.CalcImageHash(f'photo_temp/{self.product_title}.jpg')
                hash2 = self.CalcImageHash(f'photo_temp/{self.product_title}_{suffix}.jpg')
                difference = self.compareHash(hash1, hash2)
            os.remove(f'photo_temp/{self.product_title}_{suffix}.jpg')
            print('Hash difference is: ', difference, f' {item["img_url"]}')
            if difference < 45:
                return True
            return False

        except Exception:
            return False


if __name__ == "__main__":
        driver = EbayScraper()
        driver.open_ebay_and_start_scraping()
