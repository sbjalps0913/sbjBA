from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import QuestionSet, Question

class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = UserCreationForm.Meta.fields

    def clean_username(self):
        return self.cleaned_data['username']
    

# 問題集作成フォーム
class CreateQuestionSetForm(forms.ModelForm):
    class Meta:
        model = QuestionSet
        fields = ['title', 'description']
        

# 問題作成フォーム
class CreateQuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['text', 'explanation']