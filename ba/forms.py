from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import QuestionSet, Question, Option, Bean

class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = UserCreationForm.Meta.fields

    def clean_username(self):
        return self.cleaned_data['username']
    
# 問題解答フォーム
class AnswerQuestionForm(forms.Form):
    answer = forms.ChoiceField(widget=forms.RadioSelect)


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
        

# 問題集更新
class UpdateQuestionSetForm(forms.ModelForm):
    class Meta:
        model = QuestionSet
        fields = ['title', 'description']        


# 問題更新
class UpdateQuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['text', 'explanation']


# 選択肢更新
class UpdateOptionForm(forms.ModelForm):
    class Meta:
        model = Option
        fields = ['text', 'is_correct']


# コーヒー豆追加
class CreateBeanForm(forms.ModelForm):
    
    PROCESSING_CHOICES = [
        ('WASHED', 'WASHED'),
        ('SEMI-WASHED', 'SEMI-WASHED'),
        ('DRIED', 'DRIED'),
        ('VARIES', 'VARIES'),
    ]
    
    processing = forms.MultipleChoiceField(choices=PROCESSING_CHOICES,widget=forms.CheckboxSelectMultiple)
    
    class Meta:
        model = Bean
        fields = '__all__'
        
    def clean_processing(self):
        data = self.cleaned_data['processing']
        return ','.join(data)


# コーヒー豆更新
class UpdateBeanForm(forms.ModelForm):
    PROCESSING_CHOICES = [
        ('WASHED', 'WASHED'),
        ('SEMI-WASHED', 'SEMI-WASHED'),
        ('DRIED', 'DRIED'),
        ('VARIES', 'VARIES'),
    ]
    
    ACIDITY_CHOICES = [
        ('HIGH', 'HIGH'),
        ('MEDIUM', 'MEDIUM'),
        ('LOW', 'LOW'),
    ]

    BODY_CHOICES = [
        ('LIGHT', 'LIGHT'),
        ('MEDIUM', 'MEDIUM'),
        ('FULL', 'FULL'),
    ]

    REGION_CHOICES = [
        ('LATIN AMERICA', 'LATIN AMERICA'),
        ('ASIA/PACIFIC', 'ASIA/PACIFIC'),
        ('AFRICA', 'AFRICA'),
        ('MULTI-REGION', 'MULTI-REGION'),
    ]
    
    processing = forms.MultipleChoiceField(choices=PROCESSING_CHOICES, widget=forms.CheckboxSelectMultiple)
    acidity = forms.ChoiceField(choices=ACIDITY_CHOICES, widget=forms.RadioSelect)
    body = forms.ChoiceField(choices=BODY_CHOICES, widget=forms.RadioSelect)
    region = forms.ChoiceField(choices=REGION_CHOICES, widget=forms.RadioSelect)

    class Meta:
        model = Bean
        fields = ['name', 'three_letters', 'roast', 'flavor', 'acidity', 'body', 'processing', 'region', 'complementary']
        widgets = {
            'roast': forms.NumberInput(attrs={'min': 1, 'max': 6}),  # ローストレベルの範囲を指定
        }
    
    def clean_processing(self):
        data = self.cleaned_data['processing']
        return ','.join(data)

        



        
        
        
        
        
        
        