import math
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver import ChromeOptions
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
import os
import sys
import random
import requests
import re
# from scrapers.cgcValueScraper import get_values_and_grades
# import cv2
# import difflib
# from PIL import Image
# import imagehash


class EbayScraper:

    def __init__(self, product_title, cgc_link, price_percentage, floor_price, min_grade, max_grade, negative_words, positive_words):
        self.scraped_items = []
        self.matched_items = []
        # self.product_title = "Avengers #8"
        # self.search_query = self.product_title + ' cgc'
        # self.min_grade = 0.0
        # self.price_percentage = 13000
        # self.floor_price = 85
        # self.max_grade = 10.0
        # self.negative_words = ''
        # self.cgc_link = 'https://comics.gocollect.com/guide/view/125070'
        print('starting scraper')
        self.product_title = product_title
        self.search_query = self.product_title + ' cgc'
        self.cgc_link = cgc_link
        self.price_percentage = int(price_percentage)
        self.floor_price = int(floor_price)
        self.min_grade = float(min_grade)
        self.max_grade = float(max_grade)
        self.negative_words = str(negative_words)
        self.positive_words = str(positive_words)

        self.grades_values, self.img_url = get_values_and_grades(self.cgc_link)
       # self.get_comics_image()
        options = ChromeOptions()
        user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36"
        options.add_argument(f'--user-agent={user_agent}')
        options.add_argument("--start-maximized")
        options.add_argument("--headless")
        # options.add_argument("--lang=en")
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
       # options.add_argument('--proxy-server=%s' % '213.189.219.231:24000')
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        options.add_argument("--disable-blink-features=AutomationControlled")
        self.driver = webdriver.Chrome(
                                       chrome_options=options)
        self.driver.set_page_load_timeout(30)

    def open_ebay_and_start_scraping(self):
        try:
            print('opening ebay')
            self.open_ebay()
            print('entering a keys')
            self.find_a_product()
            # self.switch_cost_converting()
            time.sleep(1)
            self.get_ebay_course()
            i = 1
            while True:
                print(f'page #{i}')
                i += 1
                self.scroll_page()
                time.sleep(5)
                self.scrape_items()
                is_next_page = self.move_to_the_next_page()
                if not is_next_page:
                    break

            self.scraped_items = [dict(t) for t in {tuple(d.items()) for d in self.scraped_items}]
            self.find_items_that_fit_criterias()

            # print(len(self.scraped_items))
            # print(self.matched_items)
            # print(len(self.matched_items))
        except Exception as ex:
            print('Runtime error: ', ex)
        finally:
           # self.delete_comics_image()
            self.driver.close()
            self.driver.quit()
            print(self.matched_items)
            test = self.matched_items
            self.matched_items = []
            self.scraped_items = []
            return test

    def get_ebay_course(self):
        try:
            soup = self.create_soup()
            soup = soup.find('div', class_='left-center').find('ul', id='ListViewInner')
            card = soup.find('li', class_='sresult lvresult clearfix li')
            url = card.find('h3', class_='lvtitle').find('a', class_='vip').get('href')
            r = requests.get(url)
            soup = BeautifulSoup(r.text, 'lxml')
            us_cost = float(soup.find('span', itemprop='price').get('content'))
            rub_cost = soup.find('span', id='convbidPrice') or soup.find('span', id='convbinPrice')
            rub_cost = float(rub_cost.text.replace('\xa0', '').replace(',', '.').strip().split(' ')[0])
            self.ebay_course = rub_cost / us_cost
        except Exception as ex:
            print('Error in cost converting: ', ex)

    def switch_cost_converting(self):
        while True:
            try:
                print('switching cost converting')
                time.sleep(5)
                button = self.driver.find_element_by_xpath("//span[@class='vLIST vHvr']")
                button.click()
                time.sleep(5)
                button = self.driver.find_element_by_xpath("//span[contains(.,'Customize...')]")
                button.click()
                time.sleep(5)
                button = self.driver.find_element_by_xpath("(//input[@type='checkbox'])[6]")
                button.click()
                time.sleep(5)
                button.send_keys(Keys.ENTER)
                # button = self.driver.find_element_by_xpath("//input[@class='btn-prim small']")
                # button.click()
                break
            except Exception:
                self.driver.refresh()

    def open_ebay(self):
        # self.driver.get('https://www.ebay.com/')
        self.driver.get("https://www.ebay.com/sch/ebayadvsearch")
        time.sleep(5)
        #print(self.driver.page_source)
        self.change_language()
        # button = self.driver.find_element_by_xpath("//a[@href='https://www.ebay.com/sch/ebayadvsearch']")
        # button.click()

    def change_language(self):
        while True:
            try:
                print('changing site language')
                button = self.driver.find_element_by_xpath("//a[@id='gh-eb-Geo-a-default']")
                time.sleep(1)
                button.click()
                time.sleep(1)
                button = self.driver.find_element_by_xpath("//span[@class='gh-eb-Geo-txt'][contains(.,'English')]")
                time.sleep(1)
                button.click()
                break
            except Exception as ex:
                print('Unable to change language: ', ex)
                self.driver.refresh()
                time.sleep(3)

    def find_items_that_fit_criterias(self):
        print('finding items that fit criterias')
        for item in self.scraped_items:
            if self.match_comics_name(item):
                if self.is_cgc_in_title(item):
                    grade = self.find_grade_in_title(item)
                    if grade:
                        if self.match_grade_criteria(grade):
                            if self.match_price_criteria(item, grade):
                                 self.matched_items.append(item)

    def match_positive_words_criteria(self, item):
        try:
            if len(self.positive_words) != 0:
                for word in self.positive_words.split(','):
                    if word.lower() not in item['title'].lower():
                        return False
            return True
        except Exception as ex:
            print('Error in matching positive words: ', ex)
            return False

    def match_negative_words_criteria(self, item):
        try:
            if len(self.negative_words) != 0:
                for word in self.negative_words.split(','):
                    if word.lower() in item['title'].lower():
                        return False
            return True
        except Exception as ex:
            print('Error in matching negative words: ', ex)
            return False

    def match_comics_name(self, item):
        try:
            splited_title = self.product_title.split("#")
            match = re.search(
                r'{}\b'.format(self.product_title.lower()), item['title'].lower()) or \
                    re.search(r'{}[ #%]{}\b'.format(splited_title[0].lower().strip(), splited_title[1]),
                              item['title'].lower())
            if match:
                return True
            else:
                return False
        except Exception as ex:
            print('Cannot match comics name: ', ex, item)
            return False

    def match_price_criteria(self, item, grade):
        try:
            cgc_cost = list(x for x in self.grades_values if x[0] == grade)[0][1]
            cost_that_user_willing_to_pay = (100 + self.price_percentage) * cgc_cost / 100
            floor_cost = (100 - self.floor_price) * cgc_cost / 100
           # print(f'floor cost {floor_cost}, item cost {item["cost"]}, max cost {cost_that_user_willing_to_pay} at {item["title"]}, {item["url"]}')
            if floor_cost <= item['cost'] <= cost_that_user_willing_to_pay:
                #print(f'floor cost {floor_cost}, item cost {item["cost"]}, max cost {cost_that_user_willing_to_pay} at {item["title"]}, {item["url"]}')
                return True
            return False
        except Exception as ex:
            print('Cannot match price criterias: ', ex, item['url'])
            # print(grade, item)
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
                try:
                    grade = float(match[0].split(' ')[1].replace(',', '.'))
                except:
                    grade = float(match[0].split(' ')[0].replace(',', '.'))
                return grade

            return None
        except Exception as ex:
            print('Cannot find grade in title: ', ex, match[0])
            return None

    def find_a_product(self):
        try:
            time.sleep(3)
            #print(self.driver.page_source)
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
            #search_url = "https://www.ebay.com/sch/i.html?_from=R40&_ul=BY&_nkw="
            #for nkw in self.search_query.split(' ')[:-1]:
            #    search_url += f'{nkw}+'
            #search_url += self.search_query.split(' ')[-1] + "&_in_kw=1&_ex_kw="
            #for nkw in self.negative_words.split(' ')[:-1]:
            #     search_url += f'{nkw}+'
            #search_url += self.negative_words.split(' ')[-1]
            #search_url += "&_sacat=0&_udlo=&_udhi=&_ftrt=901&_ftrv=1&_sabdlo=&_sabdhi=&_samilow=&_samihi"
            #search_url += "=&_sadis=15&_stpos=&_sargn=-1%26saslc%3D1&_salic=1&_sop=12&_dmd=1&_ipg=200"
            #search_url += "&_fosrp=1"
            #self.driver.get(search_url)
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
                    # title = card.find('h3', class_='lvtitle').find('a', class_='vip').get('data-mtdes')
                    # cost = float(
                    #     card.find('ul', class_='lvprices left space-zero').find('span', class_='bold')
                    #         .text.replace('\xa0', '').replace(
                    #         '\n', '').replace('US $', '').replace(',', '.').strip().split(' ')[-1])
                    # cost = float(
                    #    card.find('ul', class_='lvprices left space-zero').find('span', class_='bold')
                    #        .text.replace('\xa0', '').replace(
                    #        '\n', '').replace('$', '').replace(',', '').strip().split(' ')[-1])
                    cost = round(float(card.find('ul', class_='lvprices left space-zero').find('span', class_='bold').text.replace('\xa0', '').replace(',', '').strip().split(' ')[0])/self.ebay_course, 2)

                    url = card.find('h3', class_='lvtitle').find('a', class_='vip').get('href')

                    img_url = card.find('div', class_='lvpic pic img left').find('div', class_='lvpicinner full-width picW').find(
                        'img').get('src')

                    bid = card.find('ul', class_='lvprices left space-zero').find('li', class_='lvformat').text
                    bid_format = "Auction" if 'став' in bid or 'bid' in bid else "Buy it now"

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
            except Exception:
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
        os.makedirs('photo_temp/', exist_ok=True)
        r = requests.get(self.img_url)
        with open(f'photo_temp/{self.product_title}.jpg', 'wb') as f:
            f.write(r.content)

    def delete_comics_image(self):
        os.remove(f'photo_temp/{self.product_title}.jpg')

    # def CalcImageHash(self, FileName):
    #     image = cv2.imread(FileName)
    #     resized = cv2.resize(image, (8, 8), interpolation=cv2.INTER_AREA)
    #     gray_image = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
    #     avg = gray_image.mean()  # Среднее значение пикселя
    #     ret, threshold_image = cv2.threshold(gray_image, avg, 255, 0)  # Бинаризация по порогу
    #
    #     # Рассчитаем хэш
    #     _hash = ""
    #     for x in range(8):
    #         for y in range(8):
    #             val = threshold_image[x, y]
    #             if val == 255:
    #                 _hash = _hash + "1"
    #             else:
    #                 _hash = _hash + "0"
    #
    #     return _hash

    # def compareHash(self, hash1, hash2):
    #     return math.fabs(hash1 - hash2)
    #
    # def compare_photos(self, item):
    #     try:
    #         r = requests.get(item['img_url'])
    #         suffix = random.randint(10000, 100000)
    #         with open(f'photo_temp/{self.product_title}_{suffix}.jpg', 'wb') as f:
    #             f.write(r.content)
    #             hash1 = imagehash.average_hash(Image.open(f'photo_temp/{self.product_title}.jpg'))
    #             hash2 = imagehash.average_hash(Image.open(f'photo_temp/{self.product_title}_{suffix}.jpg'))
    #             difference = self.compareHash(hash1, hash2)
    #         print(item['title'], ' Hash difference is: ', difference, f' {item["img_url"]}')
    #         if difference < 50:
    #             return True
    #         return False
    #     except Exception as ex:
    #         print('Error in img... ', ex, item['img_url'])
    #         return False
    #     finally:
    #         try:
    #             os.remove(f'photo_temp/{self.product_title}_{suffix}.jpg')
    #         except Exception:
    #             pass


def get_values_and_grades(url):
    try:
        options = ChromeOptions()
        options.add_argument("--start-maximized")
        options.add_argument("--headless")
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')

        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        options.add_argument("--disable-blink-features=AutomationControlled")
        driver = webdriver.Chrome(
                                       options=options)
        driver.set_page_load_timeout(30)

        driver.get("https://gocollect.com/login")
        button = driver.find_element_by_xpath("//input[@name='email']")
        button.click()
        button.send_keys("kardashi@gmail.com")
        button = driver.find_element_by_xpath("//input[@name='password']")
        button.click()
        button.send_keys("A010101a", Keys.ENTER)

        time.sleep(1)
        if "app" not in url:
            url = "gocollect.com/app/".join(url.split("gocollect.com/"))
        driver.get(url)
        time.sleep(1)

        soup = BeautifulSoup(driver.page_source, 'lxml')


        try:
            img_url = soup.find('div', class_='p-4 grid grid-cols-12 gap-8 flex items-center').find(
                'img', class_='mx-auto w-48 h-auto rounded-md shadow-md').get('src')
            print(img_url)
        except Exception as ex:
            print('img: ', ex)
            img_url = None

        containers = soup.find('ul', class_='border-t border-gray-200 divide-y divide-gray-200').find_all('li')
        values_and_grades = []
        try:
            for container in containers:
                try:
                    grade = float(container.find('div', class_='col-span-2 md:col-span-1 text-2xl md:text-3xl').text.strip())
                    value = container.find('div', class_="text-right grid grid-cols-12 gap-x-4").find_all('div', class_='col-span-4')[-1].find('div', class_='text-sm text-gray-600')
                    # if value is None:
                    #     value = container.find('div', class_='col-5 col-xl-6 pr-xl-0 text-right').find('div', class_='col-12 col-xl-7 text-muted')
                    value = value.text.strip().rstrip('*').lstrip('$')
                    value = float(''.join(value.split(',')).replace(',', '.'))
                    values_and_grades.append((grade, value))
                except Exception:
                    pass
        except Exception:
            values_and_grades = None
    except Exception as ex:
        print(ex)
        values_and_grades, img_url = None, None
    finally:
        driver.close()
        driver.quit()
        return values_and_grades, img_url


if __name__ == "__main__":
        driver = EbayScraper(product_title = "Avengers #4", min_grade = 0.0, price_percentage = 13000,
                             floor_price = 85, max_grade = 10.0, negative_words = '', positive_words = '',
                             cgc_link = 'https://comics.gocollect.com/guide/view/124741')
        matched_items = driver.open_ebay_and_start_scraping()
        for item in matched_items:
            print(item)
