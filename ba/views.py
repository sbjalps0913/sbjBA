from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth.forms import UserCreationForm
from django.views import View
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic.edit import CreateView, FormView
from django.views.generic.detail import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import UserProfile

# Create your views here.

# スタート画面
class StartView(View):
    template_name = 'ba/ba_start.html'
    
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)
    
    
# 新規登録画面
class RegisterView(CreateView):
    template_name = 'ba/ba_register.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('ba:login')

    def form_valid(self, form):
        response = super().form_valid(form)
        # ここで必要に応じてユーザーに関連するデータを追加できます
        
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


# 管理者用ログイン画面
class LoginManagerView(LoginView):
    template_name = 'ba/ba_manager_login.html'
    
    def get_success_url(self):
        return reverse_lazy('ba:home_manager')



# 管理者用ホーム画面
class HomeManagerView(LoginRequiredMixin, View):
    template_name = 'ba/ba_manager_home.html'
    login_url = '/ba/login_manager/'  # ログインしていない場合のリダイレクト先

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)
    
    
    
    


