from .models import SnipeModel, EbayScraperResult
from celery import shared_task
from .scrapers.ebayScraper import EbayScraper


class EbayScraperTask:
    def start_point(self, snipe):
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
        for comics in result:
            EbayScraperResult.objects.get_or_create(scraper_model=snipe, title=comics['title'], price=price['cost'],
                                                    bid_format=comics['bid_format'], comics_url=comics['url'],
                                                    comics_img_url=comics['comics_img_url'])


@shared_task
def start_point_ebay_scrapers():
    print(f'found {len(SnipeModel.objects.all())} snipemodels')
    scraper = EbayScraperTask()
    snipes = SnipeModel.objects.all()
    for snipe_object in snipes:
        scraper.start_point(snipe_object)

@shared_task
def test():
    print('govno')
