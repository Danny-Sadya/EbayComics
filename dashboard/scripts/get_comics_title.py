import requests
from bs4 import BeautifulSoup


def get_comics_title(url):
    req = requests.get(url)
    soup = BeautifulSoup(req.text, 'lxml')

    title = soup.find('section', class_='bg-white py-3 mb-3 shadow').find(
        'div', class_='col-9 col-md-10 col-xl-11').find('h1', class_='h2 mb-1').text

    return title


if __name__ == "__main__":
    pass