# Generated by Django 3.2.7 on 2021-10-24 21:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0008_snipemodel_search_query'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='snipemodel',
            name='search_query',
        ),
    ]
