# Generated by Django 3.2.7 on 2021-10-24 19:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0007_auto_20211020_2135'),
    ]

    operations = [
        migrations.AddField(
            model_name='snipemodel',
            name='search_query',
            field=models.CharField(blank=True, default='finding search query...', max_length=255, null=True),
        ),
    ]
