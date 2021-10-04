import requests
from bs4 import BeautifulSoup


def get_values_and_grades(url):
    try:
        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'lxml')

        try:
            img_url = soup.find('section', class_='bg-white py-3 mb-3 shadow').find('div', class_='container').find(
                'div', class_='col-3 col-md-2 col-xl-1').find('img').get('src')
        except Exception:
            img_url = None

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

        return values_and_grades, img_url
    except Exception:
        return None, None


if __name__ == "__main__":
    test_url = 'https://comics.gocollect.com/guide/view/124346'
    value, img_url = get_values_and_grades(test_url)
    print(value)
    print(img_url)
