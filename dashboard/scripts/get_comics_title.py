import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver import ChromeOptions
from selenium.webdriver.common.keys import Keys
import os
import requests


def get_comics_title(url):
    try:
        options = ChromeOptions()
        options.add_argument("--start-maximized")
        options.add_argument("--headless")
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--no-sandbox')
    
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
        if "app" not in url:
            url = "gocollect.com/app/".join(url.split("gocollect.com/"))
        driver.get(url)
    
        time.sleep(1)    
        try:
            title = driver.find_element_by_xpath("(//div[@class='text-xl sm:text-2xl font-extrabold tracking-tight text-gray-900'])[1]").text
        except Exception:
            soup = BeautifulSoup(driver.page_source, 'lxml')
            title = soup.find('div', class_='bg-white mb-4 bg-gradient-to-t from-gray-50 to-gray-100').find(
                'div', class_='text-xl sm:text-2xl font-extrabold tracking-tight text-gray-900').text.strip()

        try:
            soup = BeautifulSoup(driver.page_source, 'lxml')
            img_url = soup.find('div', class_='p-4 grid grid-cols-12 gap-8 flex items-center').find(
                'img', class_='mx-auto w-48 h-auto rounded-md shadow-md').get('src')
            r = requests.get(img_url)
            img = r.content
        except Exception as ex:
            img = None

    
    except:
        pass
    finally:
        driver.close()
        driver.quit()
        return title, img


if __name__ == "__main__":
    print(get_comics_title("https://gocollect.com/app/comic/avengers-2"))
