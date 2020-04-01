from django.http import HttpRequest
from django.shortcuts import render
from django.urls import path
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from WEB import models


# t = models.Tag(title='algorithm', count='9')
# t.save()
# ta = models.Tag(title='web', count='3')
# ta.save()
u = models.UserProfile.objects.get(pk=1)
a = models.Answer(author=u, text='answer', like=3)
# q = models.Question(author=u, text='texno', title='WithTags', like=1)
q = models.Question.objects.get(pk=27)

# q.save()
# q.tags.add(t)
# q.tags.add(ta)
# q.save()


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
    rendered_data = {"questions": paginated_data, "tags": models.Tag.objects.bestTags()}
    return render(request, 'MainPage.html', rendered_data)


def hot(request):
    articles = models.Question.objects.best_published()
    paginated_data = paginate(articles, request)
    rendered_data = {"questions": paginated_data, "tags": models.Tag.objects.bestTags()}

    return render(request, 'MainPage.html', rendered_data)


def tag(request, tagid):
    articles = models.Question.objects.by_tag(tagid)
    paginated_data = paginate(articles, request)
    rendered_data = {"questions": paginated_data, "tags": models.Tag.objects.bestTags()}
    return render(request, 'MainPageByTag.html', rendered_data)


def question(request, qid):
    question = models.Question.objects.get(pk=qid)
    answers = models.Answer.objects.by_question(qid)
    paginated_data = paginate(answers, request)
    rendered_data = {"question": question, "answers" : paginated_data, "tags": models.Tag.objects.bestTags()}
    return render(request, 'AddPageInfo.html',
        rendered_data
    )


def login(request):
    return render(request, 'LoginPage.html', {"tags": models.Tag.objects.bestTags()})


def signup(request):
    return render(request, 'Registration.html', {"tags": models.Tag.objects.bestTags()})


def ask(request):
    return render(request, 'AddPage.html', {"tags": models.Tag.objects.bestTags()})


def setting(request):
    return render(request, 'SettingsPage.html', {"tags": models.Tag.objects.bestTags()})
