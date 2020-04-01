# Generated by Django 3.0.4 on 2020-04-01 07:27

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('WEB', '0009_remove_question_dislike'),
    ]

    operations = [
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('like', models.IntegerField(default=0, verbose_name='Answer_like')),
                ('text', models.TextField(verbose_name='Текст ответа')),
                ('date_published', models.DateTimeField(default=datetime.datetime(2020, 4, 1, 7, 27, 32, 352852, tzinfo=utc), verbose_name='Дата ответа')),
                ('is_correct', models.BooleanField(default=False)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='WEB.Question')),
            ],
            options={
                'verbose_name': 'Ответ',
                'verbose_name_plural': 'Ответы',
            },
        ),
    ]
