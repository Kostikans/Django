from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from WEB import models
from random import choice
from faker import Faker

f = Faker()


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('--authors', type=int)
        parser.add_argument('--questions', type=int)
        parser.add_argument('--answers', type=int)
        parser.add_argument('--tags', type=int)

    def fill_authors(self, cnt):
        objs = list()
        users = list()
        for i in range(cnt):
            users.append(models.UserProfile(username=f.name()))
            objs.append(models.Author(
                rating=f.random_int(min=-100, max=100),
                name=f.name()
            ))

        models.UserProfile.objects.bulk_create(objs=users)
        models.Author.objects.bulk_create(objs=objs)

    def fill_tags(self, cnt):
        objs = list()
        for i in range(cnt):
           objs.append(models.Tag(
                title=f.sentence()[:128],
                count=f.random_int(min=0, max=10)
            ))
        models.Tag.objects.bulk_create(objs=objs)

    def fill_questions(self, cnt):
        objs = list()
        authors = models.Author.objects.all()
        for i in range(cnt):
            objs.append(models.Question(
                author=choice(authors),
                title=f.sentence()[:28],
                text=f.sentence()[:46],
            ))
        models.Question.objects.bulk_create(objs=objs)
        objects = models.Question.objects.all()
        tags = models.Tag.objects.all()
        for i in range(cnt):
            objects[i].tags.add(choice(tags))
        models.Question.objects.update()

    def fill_answers(self, cnt):
        objs = list()
        authors = models.Author.objects.all()
        questions = models.Question.objects.all()
        for i in range(cnt):
            objs.append(models.Answer(
                text=f.sentence()[:46],
                author=choice(authors)
            ))
            objs[i].question = choice(questions)
        models.Answer.objects.bulk_create(objs=objs)


    def handle(self, *args, **options):
        self.fill_authors(options.get('authors', 15))
        self.fill_tags(options.get('tags', 15))
        self.fill_questions(options.get('questions', 15))
        self.fill_answers(options.get('answers', 15))
