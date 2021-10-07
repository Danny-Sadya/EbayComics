from .models import SnipeModel, EbayScraperResult
from celery import shared_task


class EbayScraper:
    def start_point(self, snipe):
        print('work')


@shared_task
def start_point_ebay_scrapers():
    scraper = EbayScraper()
    scraper.start_point()
