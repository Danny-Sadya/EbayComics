# Generated by Django 3.2.7 on 2021-10-04 10:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0002_alter_snipemodel_lowest_grade'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='snipemodel',
            name='list_of_grades',
        ),
        migrations.AddField(
            model_name='snipemodel',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='image'),
        ),
    ]
