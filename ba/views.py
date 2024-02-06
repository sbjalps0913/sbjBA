from django.shortcuts import get_object_or_404, render, redirect, reverse
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.http import HttpResponseRedirect
from django.views import View
from django.views.generic.list import ListView
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import DeleteView
from django.views.generic.edit import CreateView, FormView, UpdateView
from django.views.generic.detail import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import UserProfile, QuestionSet, Question, Option
from .forms import RegisterForm, CreateQuestionSetForm, CreateQuestionForm, OptionForm, UpdateQuestionSetForm, UpdateQuestionForm, UpdateOptionForm

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
        context['option1'] = OptionForm(prefix='option1')
        context['option2'] = OptionForm(prefix='option2')
        context['option3'] = OptionForm(prefix='option3')
        context['option4'] = OptionForm(prefix='option4')
        return context

    def form_valid(self, form):
        question_set_id = self.kwargs['pk']
        question_set = get_object_or_404(QuestionSet, id=question_set_id)
        form.instance.question_set = question_set
        
        # 問題を保存
        form.save()
        
        # 選択肢を保存
        option1 = OptionForm(self.request.POST, prefix='option1')
        option2 = OptionForm(self.request.POST, prefix='option2')
        option3 = OptionForm(self.request.POST, prefix='option3')
        option4 = OptionForm(self.request.POST, prefix='option4')

        if option1.is_valid() and option2.is_valid() and option3.is_valid() and option4.is_valid():
            option1.instance.question = form.instance
            option1.save()

            option2.instance.question = form.instance
            option2.save()

            option3.instance.question = form.instance
            option3.save()

            option4.instance.question = form.instance
            option4.save()
        
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
    

# 【管理者】問題詳細画面
class QuestionDetailView(LoginRequiredMixin, DetailView):
    model = Question
    template_name = 'ba/ba_manager_Question_detail.html'
    context_object_name = 'question'
    login_url = '/ba/login_manager/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        question = self.get_object()
        options = question.option_set.all()
        context['options'] = options
        return context


# 【管理者】問題集更新画面
class UpdateQuestionSetView(LoginRequiredMixin, UpdateView):
    model = QuestionSet
    template_name = 'ba/ba_manager_update_QuestionSet.html'
    form_class = UpdateQuestionSetForm
    login_url = '/ba/login_manager/'

    def get_object(self, queryset=None):
        pk = self.kwargs.get('pk')
        return get_object_or_404(QuestionSet, pk=pk)
    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['question_set'] = self.get_object()
        return context
    
    
    def get_success_url(self):
        question_set_id = self.kwargs['pk']
        return reverse('ba:question_set_detail', kwargs={'pk': question_set_id})


# 【管理者】問題更新画面
class UpdateQuestionView(LoginRequiredMixin, UpdateView):
    model = Question
    template_name = 'ba/ba_manager_update_Question.html'
    form_class = UpdateQuestionForm
    success_url = reverse_lazy('ba:question_set_list')
    login_url = '/ba/login_manager/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        question = self.get_object()
        options = Option.objects.filter(question=question)
        context['options'] = options
        return context


# 【管理者】選択肢更新画面
class UpdateOptionView(LoginRequiredMixin, UpdateView):
    model = Option
    template_name = 'ba/ba_manager_update_Option.html'
    form_class = UpdateOptionForm
    success_url = reverse_lazy('ba:question_set_list')
    login_url = '/ba/login_manager/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        options = self.get_object()
        context['options'] = options
        return context


# 【管理者】問題削除画面
class DeleteQuestionView(DeleteView):
    model = Question
    template_name = 'ba/ba_manager_delete_Question.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        #return queryset.filter(created_by=self.request.user)  # ログインユーザーが作成した問題のみ削除可能
        return queryset

    def get_success_url(self):
        # 問題削除後のリダイレクト先を設定
        return reverse_lazy('ba:question_set_detail', kwargs={'pk': self.object.question_set.id})




















































    
    
    
    


