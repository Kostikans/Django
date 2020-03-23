from django.http import HttpRequest
from django.shortcuts import render
from django.urls import path
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

questions = []
for i in range(1,30):
    questions.append({'id' : i,'title': f'question # {i}'})



def paginate(objects_list, request):
    paginator = Paginator(objects_list, 4)
    page = request.GET.get('page')
    try:
         quests = paginator.get_page(page)

    except PageNotAnInteger:
        quests = paginator.page(1)

    except EmptyPage:
        quests = paginator.page(paginator.num_pages)
    return quests

def MainPage(request):
    pagData = paginate(questions, request)
    rendered_data = {"questions": pagData}
    return render(request, 'MainPage.html', rendered_data)

# def MainPage(request):
#
#     return render(request, 'MainPage.html', {
#          'questions': questions,
#      })


def hot(request):
    return render(request, 'MainPage.html', {

        'questions': questions,
    })


def tag(request):
    return render(request, 'MainPageByTag.html', {

        'questions': questions,
    })


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
