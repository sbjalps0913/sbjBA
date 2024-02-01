from django.shortcuts import get_object_or_404, render, redirect, reverse
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.http import HttpResponseRedirect
from django.views import View
from django.views.generic.list import ListView
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic.edit import CreateView, FormView
from django.views.generic.detail import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import UserProfile, QuestionSet, Question
from .forms import RegisterForm, CreateQuestionSetForm, CreateQuestionForm

# Create your views here.

# スタート画面
class StartView(View):
    template_name = 'ba/ba_start.html'
    
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)
    
    
# 新規登録画面
class RegisterView(CreateView):
    template_name = 'ba/ba_register.html'
    form_class = RegisterForm
    success_url = reverse_lazy('ba:login')

    def form_valid(self, form):
        response = super().form_valid(form)
        # ここで必要に応じてユーザーに関連するデータを追加できます
        
        
        # UserProfileがまだ存在しない場合にのみ作成する
        if not hasattr(self.object, 'userprofile'):
            UserProfile.objects.create(user=self.object)
        
        return response


# 通常ユーザ用ログイン画面
class LoginView(LoginView):
    template_name = 'ba/ba_login.html'
    
    def get_success_url(self):
        return reverse_lazy('ba:home')
    
    
# ログアウト画面    
class LogoutView(LogoutView):
    template_name = 'ba/ba_logout.html'
    next_page = reverse_lazy('ba:start')


# ホーム画面
class HomeView(LoginRequiredMixin, View):
    template_name = 'ba/ba_home.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)
    
    def post(self, request, *args, **kwargs):
        # ログアウトのPOSTリクエストが来た場合はログアウト確認画面にリダイレクト
        return redirect('ba:logout')


# 【管理者】ログイン画面
class LoginManagerView(LoginView):
    template_name = 'ba/ba_manager_login.html'
    
    
    def form_valid(self, form):
        # 認証フォームを使用してユーザーを認証
        user = form.get_user()

        # ユーザーが存在し、かつ is_master が True の場合にログイン
        if user and user.userprofile.is_manager:
            login(self.request, user)
            return HttpResponseRedirect(self.get_success_url())
        else:
            # 認証失敗時の処理
            form.add_error(None, '管理者としてログインする権限がありません。')

        return super().form_invalid(form)

    def get_success_url(self):
        return reverse_lazy('ba:home_manager')



# 【管理者】ホーム画面
class HomeManagerView(LoginRequiredMixin, View):
    template_name = 'ba/ba_manager_home.html'
    login_url = '/ba/login_manager/'  # ログインしていない場合のリダイレクト先

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)
    

# 【管理者】問題集作成画面
class CreateQuestionSetView(LoginRequiredMixin, CreateView):
    template_name = 'ba/ba_manager_create_QuestionSet.html'
    form_class = CreateQuestionSetForm
    success_url = reverse_lazy('ba:question_set_list')
    login_url = '/ba/login_manager/'

    def form_valid(self, form):
        # ログインユーザーが管理者かどうかのチェック
        if not self.request.user.userprofile.is_manager:
            return self.handle_no_permission()

        # ログインユーザーを問題集の作成者に設定
        form.instance.created_by = self.request.user
        form.instance.save()
        
        return super().form_valid(form)
    
    
# 【管理者】問題作成画面
class CreateQuestionView(LoginRequiredMixin, CreateView):
    model = Question
    template_name = 'ba/ba_manager_create_Question.html'
    form_class = CreateQuestionForm
    login_url = '/ba/login_manager/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        question_set_id = self.kwargs['pk']
        question_set = get_object_or_404(QuestionSet, id=question_set_id)
        context['question_set'] = question_set
        return context

    def form_valid(self, form):
        question_set_id = self.kwargs['pk']
        question_set = get_object_or_404(QuestionSet, id=question_set_id)
        form.instance.question_set = question_set
        return super().form_valid(form)

    def get_success_url(self):
        question_set_id = self.kwargs['pk']
        return reverse('ba:question_set_detail', kwargs={'pk': question_set_id})


# 【管理者】問題集一覧画面
class QuestionSetListView(LoginRequiredMixin, ListView):
    template_name = 'ba/ba_manager_questionlist.html'
    model = QuestionSet
    context_object_name = 'question_sets'
    login_url = '/ba/login_manager/'
    
    
# 【管理者】問題集詳細画面
class QuestionSetDetailView(LoginRequiredMixin, DetailView):
    model = QuestionSet
    template_name = 'ba/ba_manager_QuestionSet_detail.html'
    context_object_name = 'question_set'
    login_url = '/ba/login_manager/'













    
    
    
    


