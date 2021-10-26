from django.db import models
from django.contrib.auth.models import AbstractUser


def Reverse(tuples):
    new_tup = tuples[::-1]
    return new_tup



grades_list = []
for i in range(0, 101):
    grades_list.append((str((float(i/10))), str(float(i/10))))

GRADES = tuple(grades_list)

PERMISSION_LEVEL = (
    ('r', 'Readonly'),
    ('rw', 'Read+Write'),
)

class User(AbstractUser):

    class Meta:
        # permissions = models.CharField(max_length=255, choices=PERMISSION_LEVEL, null=False, blank=False)
        permissions = PERMISSION_LEVEL


# Create your models here.
class SnipeModel(models.Model):
    title = models.CharField(default='finding title...', null=True, blank=True, max_length=255)
    gocollect_link = models.URLField(null=False, blank=False)
    price_percentage = models.IntegerField(null=False)
    floor_price = models.IntegerField(null=True, blank=False, default=85)
    lowest_grade = models.CharField(default='0.0', choices=Reverse(GRADES), blank=False, null=False, max_length=255)
    highest_grade = models.CharField(default='10.0',choices=Reverse(GRADES), blank=False, null=False, max_length=255)
    negative_words = models.CharField(blank=True, null=True, max_length=255)
    positive_words = models.CharField(blank=True, null=True, max_length=255)
    image = models.ImageField(upload_to='image', blank=True, null=True)
    # list_of_grades = models.CharField(blank=True, null=True, max_length=255)

    def __str__(self):
        return(str(self.title))


class EbayScraperResult(models.Model):
    scraper_model = models.ForeignKey(SnipeModel, on_delete=models.CASCADE)
    title = models.CharField(null=True, blank=True, max_length=255)
    price = models.IntegerField(null=True, blank=True)
    max_price = models.IntegerField(null=True, blank=True)
    bid_format = models.CharField(null=True, blank=True, max_length=255)
    comics_url = models.CharField(null=True, blank=True, max_length=255)
    comics_img_url = models.CharField(null=True, blank=True, max_length=255)
    is_already_in_gixen = models.BooleanField(default=False, null=True, blank=True)

    def __str__(self):
        return(f'{self.scraper_model.title} | {str(self.title)}')
