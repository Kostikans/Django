from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import datetime
from django.conf import settings
from django.utils import timezone


class Author(models.Model):
    name = models.CharField(max_length=255, verbose_name='Имя', unique=True)

    def __str__(self):
        return self.name


class UserProfile(AbstractUser):
    avatar = models.ImageField(upload_to='uploads/%Y/%m/%d/')


class Tag(models.Model):
    title = models.CharField(max_length=120, verbose_name=u"Заголовок ярлыка", default="Texno")

    count = models.IntegerField(verbose_name="Число упоминаний", default=0)

    def __str__(self):
        return self.title, self.count


class QuestionManager(models.Manager):
    def new_published(self):
        return self.filter(
            is_active=True,
            create_date=datetime.now(tz=timezone.utc),
        ).order_by("-create_date")

    def best_published(self):
        test = list(self.filter(is_active=True))
        test = sorted(test, key=lambda x: x.like.count(), reverse=True)
        return test

    def by_tag(self, tag):
        return self.filter(is_active=True, tags=tag)


class Question(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)

    title = models.CharField(max_length=120, verbose_name=u"Заголовок вопроса")
    text = models.TextField(verbose_name=u"Полное описание вопроса")
    image = models.ImageField(default=True, upload_to='uploads/%Y/%m/%d/')

    create_date = models.DateTimeField(default=datetime.now, verbose_name=u"Время создания вопроса")

    is_active = models.BooleanField(default=True, verbose_name=u"Доступность вопроса")

    tags = models.ManyToManyField(Tag, blank=True)

    objects = QuestionManager()

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-create_date']
