from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.forms import ModelForm

from WEB.models import Question, UserProfile, Answer


class LoginForm(forms.Form):
    username = forms.CharField(max_length=20)
    password = forms.CharField(widget=forms.PasswordInput)

    def clean_username(self):
        username = self.cleaned_data["username"]
        if ' ' in username:
            self.add_error(username, 'username contains whitespaces')
        else:
            return username

    def clean_password(self):
        password = self.cleaned_data["password"]
        return password


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['title', 'text', 'tags']

    def __init__(self, Author, *args, **kwargs):
        self.Author = Author
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        question = super().save(commit=False)
        question.author = self.Author
        if commit:
            question.save()
        for tag in self.cleaned_data.get("tags"):
            question.tags.add(tag)

        return question


class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['text']

    def __init__(self, Author, question_id, *args, **kwargs):
        self.Author = Author
        self.question = Question.objects.get(pk=question_id)
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        answer = super().save(commit=False)
        answer.author = self.Author
        answer.question = self.question
        if commit:
            answer.save()
        return answer


class RegistrationForm(forms.ModelForm):
    login = forms.CharField(max_length=20)
    email = forms.EmailField(widget=forms.EmailInput)
    nickname = forms.CharField(max_length=20)
    password = forms.CharField(widget=forms.PasswordInput)
    password_confirm = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = UserProfile
        fields = ('avatar',)

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.fields['avatar'].required = False

    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.clean_nickname()
        user.username = self.clean_login()
        user.email = self.clean_email()
        user.password = self.clean_password()
        user.avatar = self.clean_avatar()
        if commit:
            user.save()
        return user

    def clean_avatar(self):
        avatar = self.cleaned_data["avatar"]
        return avatar

    def clean_nickname(self):
        return self.cleaned_data["nickname"]

    def clean_login(self):
        login = self.cleaned_data["login"]
        return login

    def clean_email(self):
        email = self.cleaned_data["email"]
        validate_email(email)
        return email

    def clean_password(self):
        return self.cleaned_data["password"]


class SettingsForm(forms.ModelForm):
    email = forms.EmailField(widget=forms.EmailInput)
    nickname = forms.CharField(max_length=20)
    password = forms.CharField(widget=forms.PasswordInput)
    password_confirm = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = UserProfile
        fields = ('avatar',)

    def __init__(self, *args, **kwargs):
        super(SettingsForm, self).__init__(*args, **kwargs)
        self.fields['avatar'].required = False

    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.clean_nickname()
        user.email = self.clean_email()
        user.password = self.clean_password()
        user.avatar = self.clean_avatar()
        if commit:
            user.save()
        return user

    def clean_avatar(self):
        avatar = self.cleaned_data["avatar"]
        return avatar

    def clean_nickname(self):
        return self.cleaned_data["nickname"]

    def clean_login(self):
        login = self.cleaned_data["login"]
        return login

    def clean_email(self):
        email = self.cleaned_data["email"]
        validate_email(email)
        return email

    def clean_password(self):
        return self.cleaned_data["password"]
