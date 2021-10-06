import requests
from bs4 import BeautifulSoup


def get_title_values_and_grades_img(url):
    try:
        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'lxml')

        try:
            title = soup.find('section', class_='bg-white py-3 mb-3 shadow').find(
                'div', class_='col-9 col-md-10 col-xl-11').find('h1', class_='h2 mb-1').text
        except Exception:
            title = None

        try:
            img = soup.find('section', class_='bg-white py-3 mb-3 shadow').find('div', class_='container').find('div', class_='col-3 col-md-2 col-xl-1').find('img').get('src')
        except Exception:
            img = None

        soup = soup.find('div', class_='container mt-2').find('div', class_='col-12 col-md-6').find('div', class_='tab-pane active')
        containers = soup.find('ul', class_='list-group mb-1').find_all('li', class_='list-group-item')[1:]
        values_and_grades = []
        try:
            for container in containers:
                try:
                    container = container.find('div', class_='row')
                    grade = float(container.find('div', class_='col-3 col-xl-2').text.strip())
                    value = container.find('div', class_='col-5 col-xl-6 pr-xl-0 text-right').find('div', class_='col-12 col-xl-7')
                    if value is None:
                        value = container.find('div', class_='col-5 col-xl-6 pr-xl-0 text-right').find('div', class_='col-12 col-xl-7 text-muted')
                    value = value.text.strip().rstrip('*').lstrip('$')
                    value = float(''.join(value.split(',')).replace(',', '.'))
                    values_and_grades.append((grade, value))
                except Exception:
                    pass

        except Exception:
            values_and_grades = None

        return title, values_and_grades, img
    except Exception:
        return None, None, None
