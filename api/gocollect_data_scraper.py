import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver import ChromeOptions
from selenium.webdriver.common.keys import Keys
import os


def get_title_values_and_grades_img(url):
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

        time.sleep(1)
        if "app" not in url:
            url = "gocollect.com/app/".join(url.split("gocollect.com/"))
        driver.get(url)
        time.sleep(3)

        soup = BeautifulSoup(driver.page_source, 'lxml')

        try:
            title = soup.find('div', class_='bg-white mb-4 bg-gradient-to-t from-gray-50 to-gray-100').find(
                'div', class_='text-xl sm:text-2xl font-extrabold tracking-tight text-gray-900').text.strip()
        except Exception:
            title = None

        try:
            img = soup.find('div', class_='p-4 grid grid-cols-12 gap-8 flex items-center').find(
                'img', class_='mx-auto w-48 h-auto rounded-md shadow-md').get('src')
        except Exception as ex:
            img = None
            
        try:
            containers = soup.find('ul', class_='border-t border-gray-200 divide-y divide-gray-200').find_all('li')
            values_and_grades = []
            try:
                for container in containers:
                    try:
                        grade = float(
                            container.find('div', class_='col-span-2 md:col-span-1 text-2xl md:text-3xl').text.strip())
                        value = container.find('div', class_="text-right grid grid-cols-12 gap-x-4").find_all('div',
                                                                                                              class_='col-span-4')[
                            -1].find('div', class_='text-sm text-gray-600')
                        # if value is None:
                        #     value = container.find('div', class_='col-5 col-xl-6 pr-xl-0 text-right').find('div', class_='col-12 col-xl-7 text-muted')
                        value = value.text.strip().rstrip('*').lstrip('$')
                        value = float(''.join(value.split(',')).replace(',', '.'))
                        values_and_grades.append((grade, value))
                    except Exception:
                        pass
    
            except Exception:
                values_and_grades = None
        except Exception:
            values_and_grades = None

        
    except Exception as ex:
        print(ex)
        title, values_and_grades, img = None, None, None
    finally:
        driver.close()
        driver.quit()
        return title, values_and_grades, img


if __name__ == '__main__':
    pass


