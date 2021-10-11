from django.db import models
from django.contrib.auth.models import AbstractUser


def Reverse(tuples):
    new_tup = tuples[::-1]
    return new_tup



GRADES = (
    ('0.5', '0.5'),
    ('1.0', '1.0'),
    ('1.5', '1.5'),
    ('1.8', '1.8'),
    ('2.0', '2.0'),
    ('2.5', '2.5'),
    ('3.0', '3.0'),
    ('3.5', '3.5'),
    ('4.0', '4.0'),
    ('4.5', '4.5'),
    ('5.0', '5.0'),
    ('5.5', '5.5'),
    ('6.0', '6.0'),
    ('6.5', '6.5'),
    ('7.0', '7.0'),
    ('7.5', '7.5'),
    ('8.0', '8.0'),
    ('8.5', '8.5'),
    ('9.0', '9.0'),
    ('9.2', '9.2'),
    ('9.4', '9.4'),
    ('9.6', '9.6'),
    ('9.8', '9.8'),
)

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
    lowest_grade = models.CharField(default='0', choices=GRADES, blank=False, null=False, max_length=255)
    highest_grade = models.CharField(default='10',choices=Reverse(GRADES), blank=False, null=False, max_length=255)
    negative_words = models.CharField(blank=True, null=True, max_length=255)
    positive_words = models.CharField(blank=True, null=True, max_length=255)
    image = models.ImageField(upload_to='image', blank=True, null=True)
    # list_of_grades = models.CharField(blank=True, null=True, max_length=255)

    def __str__(self):
        return(str(self.pk))


class EbayScraperResult(models.Model):
    scraper_model = models.ForeignKey(SnipeModel, on_delete=models.CASCADE)
    title = models.CharField(null=True, blank=True, max_length=255)
    price = models.IntegerField(null=True, blank=True)
    bid_format = models.CharField(null=True, blank=True, max_length=255)
    comics_url = models.CharField(null=True, blank=True, max_length=255)
    comics_img_url = models.CharField(null=True, blank=True, max_length=255)
