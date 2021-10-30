from .models import SnipeModel, EbayScraperResult
from celery import shared_task
from .scrapers.ebayScraper import EbayScraper
#from multiprocessing import Pool
from billiard.pool import Pool
from billiard.pool import Lock
from billiard.context import Process
import time
import random
from functools import partial


class EbayScraperTask:
    def start_point(self, snipe):
        self.snipe = snipe
        print(f'work for {getattr(self.snipe, "title")}')
        product_title = getattr(self.snipe, "title")
        cgc_link = getattr(self.snipe, "gocollect_link")
        price_percentage = getattr(self.snipe, "price_percentage")
        floor_price = getattr(self.snipe, "floor_price")
        min_grade = getattr(self.snipe, "lowest_grade")
        max_grade = getattr(self.snipe, "highest_grade")
        negative_words = getattr(self.snipe, "negative_words")
        positive_words = getattr(self.snipe, "positive_words")
        scraper = EbayScraper(product_title, cgc_link, price_percentage, floor_price, min_grade, max_grade, negative_words, positive_words)
        result = scraper.open_ebay_and_start_scraping() 
        for comics in result:
            try:
                snipe_model = EbayScraperResult.objects.get(comics_url=comics['url'])
                snipe_model.price = comics['cost']
                snipe_model.max_price = comics['max_price']
                snipe_model.save()
                print(f'updating comic {comics["title"]}')
            except Exception:
                print(f'saving comic {comics["title"]}')
                EbayScraperResult.objects.create(scraper_model=self.snipe, title=comics['title'],
                                                 price=comics['cost'],
                                                 max_price=comics['max_price'], bid_format=comics['bid_format'],
                                                 comics_url=comics['url'], comics_img_url=comics['img_url'])
            finally:
                all_comics = EbayScraperResult.objects.filter(scraper_model=self.snipe)
                for comic in all_comics:
                    comic_url = comic.comics_url
                    try:
                        comics = [x for x in result if x['url'] == comic_url][0]
                    except Exception as ex:
                        #print(ex)
                        print(f'Comic not exist, deleting {comic.title}')
                        comic.delete()


def pool_scraper_task(snipe):
    snipe_obj = snipe
    scraper = EbayScraperTask()
    scraper.start_point(snipe_obj)


@shared_task()
def start_point_ebay_scrapers():
    print(f'found {len(SnipeModel.objects.all())} snipemodels')
    snipes = SnipeModel.objects.all()
    pool = Pool(processes=3)
    pool.map(pool_scraper_task, snipes)
    print('closing all pools')
    pool.close()
    pool.join()
    pool.terminate()
    print('all pools are closed')
    

@shared_task()
def test():
    print('govno')
