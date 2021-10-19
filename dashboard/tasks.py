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
        try:
            print(result)
        except:
            pass
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
            print(f'saving comic {comics["title"]}')
            EbayScraperResult.objects.get_or_create(scraper_model=self.snipe, title=comics['title'], price=comics['cost'],
                                                    bid_format=comics['bid_format'], comics_url=comics['url'],
                                                    comics_img_url=comics['img_url'])



def ebayScraperTask(lock):
    def start_point(snipe):
        print(f'work for {getattr(snipe, "title")}')
        product_title = getattr(snipe, "title")
        cgc_link = getattr(snipe, "gocollect_link")
        price_percentage = getattr(snipe, "price_percentage")
        floor_price = getattr(snipe, "floor_price")
        min_grade = getattr(snipe, "lowest_grade")
        max_grade = getattr(snipe, "highest_grade")
        negative_words = getattr(snipe, "negative_words")
        positive_words = getattr(snipe, "positive_words")
        scraper = EbayScraper(product_title, cgc_link, price_percentage, floor_price, min_grade, max_grade, negative_words, positive_words)
        result = scraper.open_ebay_and_start_scraping()
        lock.acquire()
        for comics in result:
            EbayScraperResult.objects.get_or_create(scraper_model=snipe, title=comics['title'], price=comics['cost'],
                                                    bid_format=comics['bid_format'], comics_url=comics['url'],
                                                    comics_img_url=comics['img_url'])
        lock.release()
    return start_point


def pool_scraper_task(snipe):
    snipe_obj = snipe
    scraper = EbayScraperTask()
    scraper.start_point(snipe_obj)


@shared_task()
def start_point_ebay_scrapers():
    print(f'found {len(SnipeModel.objects.all())} snipemodels')
    snipes = SnipeModel.objects.all()
    #lock = Lock()
    pool = Pool(processes=3)
    #func = partial(start_point, lock)
    pool.map(pool_scraper_task, snipes)
    print('closing all pools')
    pool.close()
    pool.join()
    pool.terminate()
    print('all pools are closed')
    

@shared_task()
def test():
    print('govno')
