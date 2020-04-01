from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import datetime
from django.conf import settings
from django.utils import timezone


class Author(models.Model):
    name = models.CharField(max_length=255, verbose_name=u"Имя", default="Texno")

    def __str__(self):
        return self.name


class UserProfile(AbstractUser):
    avatar = models.ImageField(upload_to='uploads/%Y/%m/%d/')
    name = models.CharField(max_length=255, verbose_name=u"Имя", default="NickName")

    def __str__(self):
        return self.avatar, self.name


class TagManager(models.Manager):
    def bestTags(self):
        return self.order_by('-count')[0:3]


class Tag(models.Model):
    title = models.CharField(max_length=120, verbose_name=u"Заголовок ярлыка", default="Texno")

    count = models.IntegerField(verbose_name="Число упоминаний", default=0)

    objects = TagManager()

    def __str__(self):
        return self.title, self.count


class QuestionManager(models.Manager):
    def best_published(self):
        return self.order_by('-like')

    def by_tag(self, tag):
        return self.filter(is_active=True, tags__title=tag)


class Question(models.Model):
    author = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

    title = models.CharField(max_length=120, verbose_name=u"Заголовок вопроса")
    text = models.TextField(verbose_name=u"Полное описание вопроса")

    create_date = models.DateTimeField(default=datetime.now, verbose_name=u"Время создания вопроса")

    is_active = models.BooleanField(default=True, verbose_name=u"Доступность вопроса")

    tags = models.ManyToManyField(Tag, blank=True)
    objects = QuestionManager()

    like = models.IntegerField(verbose_name="Число лайков", default=0)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-create_date']


class AnswerManager(models.Manager):
    def by_question(self, id):
        return self.filter(question=id)


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    author = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

    like = models.IntegerField(verbose_name="Answer_like", default=0)

    text = models.TextField(verbose_name='Текст ответа')
    date_published = models.DateTimeField(verbose_name='Дата ответа', default=datetime.now(tz=timezone.utc))

    is_correct = models.BooleanField(default=False)

    objects = AnswerManager()

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = 'Ответ'
        verbose_name_plural = 'Ответы'
