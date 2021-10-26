import os
import sys
import django

script_path = os.path.dirname(__file__)
sys.path.append(script_path)
# print(script_path)
os.environ['DJANGO_SETTINGS_MODULE']='core.settings'
django.setup()

from dashboard.models import *

snipe_model = SnipeModel(title='Avengers', gocollect_link='link.ru', price_percentage=100, floor_price=85, lowest_grade='0.0',
                         highest_grade='10.0')

result_model = EbayScraperResult(scraper_model=snipe_model, title='Avengers-bla-bla', price=1000, max_price=10000, bid_format='auction',
                                 comics_url='blabla.com', comics_img_url='bla-bla.ru')
results = EbayScraperResult.objects.all()
print(result_model.scraper_model.title)

print(result_model.is_already_in_gixen)

def add_comic_to_gixen(comic):
    url = comic.comics_url
    max_price = comic.max_price
    api_call = None
    comic.is_already_in_gixen = True
    comic.save()
    pass
