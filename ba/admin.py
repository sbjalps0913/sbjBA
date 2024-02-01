from django.contrib import admin
from .models import QuestionSet, Question, Option, UserProfile

# Register your models here.

admin.site.register(QuestionSet)
admin.site.register(Question)
admin.site.register(Option)
admin.site.register(UserProfile)