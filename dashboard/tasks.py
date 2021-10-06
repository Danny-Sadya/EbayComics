from .models import SnipeModel, EbayScraperResult
from celery import shared_task

class EbayScraper:
    def start_point(self, snipe):
        pass

@shared_task
def start_point_ebay_scrapers():
    scraper = EbayScraper()
    for snipe in SnipeModel.objects.all():
        EbayScraper.start_point(snipe)