from django.http import HttpRequest
from django.shortcuts import render
from django.urls import path
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from WEB import models
from WEB.models import Question, Tag, UserProfile

 # author = models.Author.objects.create(name='kek')
 # author.save()
 # models.Question.objects.create(author=author, title='kek', text='kek')

questions = []
for i in range(1, 30):
    questions.append({'id': i, 'title': f'question # {i}'})


def paginate(objects_list, request):
    paginator = Paginator(objects_list, 4)
    page_number = request.GET.get('page')
    try:
        page = paginator.get_page(page_number)

    except PageNotAnInteger:
        page = paginator.page(1)

    except EmptyPage:
        page = paginator.page(paginator.num_pages)
    return page


def MainPage(request):
    articles = models.Question.objects.all()
    paginated_data = paginate(articles, request)
    return render(request, 'MainPage.html', paginated_data)


def hot(request):
    articles = models.Question.objects.best_published()
    paginated_data = paginate(articles, request)
    rendered_data = {"questions": paginated_data}

    return render(request, 'MainPage.html', {
        rendered_data
    })


def tag(request):
    pagData = paginate(questions, request)
    rendered_data = {"questions": pagData}
    return render(request, 'MainPageByTag.html', rendered_data)


def question(request, qid):
    question = questions[qid - 1]
    return render(request, 'Question.html', {
        'question': question
    })


def login(request):
    return render(request, 'LoginPage.html', {})


def signup(request):
    return render(request, 'Registration.html', {})


def ask(request):
    return render(request, 'AddPage.html', {})


def setting(request):
    return render(request, 'SettingsPage.html', {})
