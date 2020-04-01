from django.contrib import admin

from WEB.models import Question, UserProfile, Tag

admin.site.register(Question)
admin.site.register(UserProfile)
admin.site.register(Tag)
