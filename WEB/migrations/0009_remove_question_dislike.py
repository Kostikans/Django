# Generated by Django 3.0.4 on 2020-03-31 18:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('WEB', '0008_auto_20200331_2048'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='question',
            name='dislike',
        ),
    ]
