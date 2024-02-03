from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import QuestionSet, Question, Option

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
        
        
# 選択肢作成フォーム
class OptionForm(forms.ModelForm):
    class Meta:
        model = Option
        fields = ['text', 'is_correct']


# 問題作成フォーム
class CreateQuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['text', 'explanation']
        
    option1 = OptionForm(prefix='option1')
    option2 = OptionForm(prefix='option2')
    option3 = OptionForm(prefix='option3')
    option4 = OptionForm(prefix='option4')
        


        
        
        
        
        
        
        