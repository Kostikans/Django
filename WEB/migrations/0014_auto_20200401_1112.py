# Generated by Django 3.0.4 on 2020-04-01 08:12

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('WEB', '0013_auto_20200401_1112'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answer',
            name='date_published',
            field=models.DateTimeField(default=datetime.datetime(2020, 4, 1, 8, 12, 22, 743356, tzinfo=utc), verbose_name='Дата ответа'),
        ),
    ]
