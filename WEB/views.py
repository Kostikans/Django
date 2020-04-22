from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest
from django.shortcuts import render, redirect
from django.urls import path, reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.urls import resolvers
from django.contrib import auth
from WEB import models
from WEB import forms


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
    rendered_data = {"questions": paginated_data, "tags": models.Tag.objects.bestTags(), "tagName": tagid}
    return render(request, 'MainPageByTag.html', rendered_data)


def question(request, qid):
    author, created = models.Author.objects.get_or_create(name=request.user.username)
    if request.POST:
        form = forms.AnswerForm(Author=author, question_id=qid, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect(request.META.get('HTTP_REFERER'))

    form = forms.AnswerForm(Author=author, question_id=qid)
    question = models.Question.objects.get(pk=qid)
    answers = question.answer_set.all()
    paginated_data = paginate(answers, request)
    rendered_data = {"question": question, "answers": paginated_data, "tags": models.Tag.objects.bestTags(),'form':form}
    return render(request, 'AddPageInfo.html', rendered_data)


def login(request):
    if request.method == "GET":
        form = forms.LoginForm()
        rendered_data = {"tags": models.Tag.objects.bestTags(), 'form': form}
        return render(request, 'LoginPage.html', rendered_data)
    else:
        form = forms.LoginForm(data=request.POST)
        if form.is_valid():
            user = auth.authenticate(request, **form.cleaned_data)
            if user is not None:
                form.clean()
                auth.login(request, user)
                return redirect('/')
            else:
                form.add_error(None, 'Неправильный логин или пароль')
    rendered_data = {"tags": models.Tag.objects.bestTags(), 'form': form}
    return render(request, 'LoginPage.html', rendered_data)


def signup(request):
    if request.method == "GET":
        form = forms.RegistrationForm()
        rendered_data = {"tags": models.Tag.objects.bestTags(), 'form': form}
        return render(request, 'Registration.html', rendered_data)

    if request.method == "POST":
        form = forms.RegistrationForm(request.POST, request.FILES)

        if form.is_valid():
            user = form.save()
            auth.login(request, user=user)
            return redirect('/')

        rendered_data = {"tags": models.Tag.objects.bestTags(), 'form': form}
        return render(request, 'Registration.html', rendered_data)


@login_required
def ask(request):
    if request.method == "GET":
        author, created = models.Author.objects.get_or_create(name=request.user.username)
        form = forms.QuestionForm(author)
        rendered_data = {"tags": models.Tag.objects.bestTags(), 'form': form}
        return render(request, 'AddPage.html', rendered_data)
    if request.method == "POST":

        author, created = models.Author.objects.get_or_create(name=request.user.username)
        form = forms.QuestionForm(Author=author, data=request.POST)
        if form.is_valid():
            question = form.save()
            return redirect(reverse('question', kwargs={'qid': question.pk}))
        rendered_data = {"tags": models.Tag.objects.bestTags(), 'form': form}
        return render(request, 'AddPage.html', rendered_data)


@login_required
def setting(request):
    if request.method == "GET":
        form = forms.SettingsForm()
        rendered_data = {"tags": models.Tag.objects.bestTags(), 'form': form}
        return render(request, 'SettingsPage.html', rendered_data)
    if request.method == "POST":
        form = forms.SettingsForm(data=request.POST,
                                  files=request.FILES,
                                  instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('/')

        rendered_data = {"tags": models.Tag.objects.bestTags(), 'form': form}
        return render(request, 'SettingsPage.html', rendered_data)


def log_out(request):
    logout(request)
    return redirect(request.META.get('HTTP_REFERER'))
