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
from django.utils import timezone

from .models import UserProfile, QuestionSet, Question, Option, Bean, Score, FinalScore, Answer
from .forms import UpdateBeanForm, RegisterForm, CreateQuestionSetForm, CreateQuestionForm, OptionForm, UpdateQuestionSetForm, UpdateQuestionForm, UpdateOptionForm, CreateBeanForm
from .forms import AnswerQuestionForm

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


# 問題集一覧画面
class QuestionSetListView(LoginRequiredMixin, ListView):
    model = QuestionSet
    template_name = 'ba/ba_QuestionSet_list.html'
    context_object_name = 'question_sets'


# 問題開始画面
class StartQuestionView(LoginRequiredMixin, DetailView):
    model = QuestionSet
    template_name = 'ba/ba_start_question.html'

    '''
    def post(self, request, *args, **kwargs):
        question_set = self.get_object()
        question = get_object_or_404(Question, question_set=question_set)
        return redirect(reverse_lazy('ba:answer_question', kwargs={'pk': question.pk}))
    '''
    
    def post(self, request, *args, **kwargs):
        question_set = self.get_object()
        first_question = question_set.question_set.first()  # 問題集に関連する最初の問題を取得
        if first_question:
            # 既存のスコアオブジェクトを取得する
            existing_score = Score.objects.filter(user=request.user, question_set=question_set).order_by('-times').first()
            # すでに同じ問題集のスコアが存在する場合
            if existing_score:
                times = existing_score.times + 1
            else:
                times = 1
            # 新しいスコアオブジェクトを作成する
            Score.objects.create(user=request.user, question_set=question_set, times=times)
            
            return redirect(reverse_lazy('ba:answer_question', kwargs={'pk': first_question.pk}))
        else:
            # 問題が存在しない場合の処理
            # 例えばエラーメッセージを表示するなど
            pass

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['question_set'] = self.object
        context['questions'] = Question.objects.filter(question_set=self.object)
        return context


# 問題詳細画面
class QuestionDetailView(LoginRequiredMixin, DetailView):
    model = Question
    template_name = 'ba/ba_Question_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # 他のコンテキストデータを必要に応じて追加
        return context


# 問題解答画面
class AnswerQuestionView(LoginRequiredMixin, FormView):
    template_name = 'ba/ba_answer_question.html'
    form_class = AnswerQuestionForm

    def dispatch(self, request, *args, **kwargs):
        self.question = get_object_or_404(Question, pk=kwargs['pk'])
        self.question_set = self.question.question_set
        return super().dispatch(request, *args, **kwargs)
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['question'] = self.question
        return kwargs
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['question'] = self.question
        context['options'] = Option.objects.filter(question=self.question)
        context['question_set'] = self.question_set
        
        context['is_last_question'] = self.is_last_question()
        context['next_question_id'] = self.get_next_question_pk()
        context['current_question_number'] = self.get_current_question_number()
        context['score'] = self.get_current_score().score
        
        # 現在の問題の正解の選択肢を取得
        correct_options = Option.objects.filter(question=self.question, is_correct=True)
        if correct_options.exists():
            context['correct_options'] = correct_options
        else:
            context['correct_options'] = '正解の選択肢がありません'
        
        return context

    def form_valid(self, form):
        selected_option_ids = form.cleaned_data['answer']    # 複数選択肢の場合、複数の選択肢がリストとして返される
        selected_option_ids = [int(id) for id in selected_option_ids]
        selected_options = Option.objects.filter(pk__in=selected_option_ids)
        
        correct_options = Option.objects.filter(question=self.question, is_correct=True)
        #print("解答",selected_option_ids)
        #print("正解",correct_options.values_list('id', flat=True))
        
        is_correct = set(selected_option_ids) == set(correct_options.values_list('id', flat=True))
        result = '正解' if is_correct else '不正解'
        
        '''
        if selected_options.is_correct:
            result = '正解'
            
            # 正解の場合は得点を加算する
            self.add_score()
        else:
            result = '不正解'
        '''
        
        # ユーザーの解答を保存
        user_answer = Answer.objects.create(
            user=self.request.user,
            question=self.question,
            is_correct=is_correct
        )
        user_answer.selected_options.set(selected_options)  # 選択された選択肢を保存
            
        # 解答が正解なら得点を加算
        if is_correct:
            self.add_score()
            
        # 解答した回数をインクリメント
        self.increment_count()    
        
        # 解答が終了した時点で日付を保存
        self.save_completion_date()
        
        context = self.get_context_data(form=form)
        context['result'] = result
        #context['selected_option'] = selected_option.text
        context['selected_options'] = selected_options
        
        # 問題集の全ての問題に回答済みの場合、FinalScoreオブジェクトを作成
        context['final_score'] = self.create_final_score()

        '''
        # 次の問題がある場合はその問題のPKを取得し、リダイレクト
        next_question_pk = self.get_next_question_pk()
        if next_question_pk:
            return redirect('ba:answer_question', pk=next_question_pk)
        '''

        return self.render_to_response(context)
    
    def is_last_question(self):
        last_question = self.question_set.question_set.last()
        return self.question == last_question
    
    # 次の問題のPKを取得
    def get_next_question_pk(self):
        next_question = self.question_set.question_set.filter(pk__gt=self.question.pk).first()
        if next_question:
            return next_question.pk
        else:
            return None
        
    
    # 現在の問題番号を取得
    def get_current_question_number(self):
        current_question_number = self.question_set.question_set.filter(pk__lte=self.question.pk).count()
        return current_question_number
    
    def add_score(self):
        # 最大のtimesを持つスコアオブジェクトを取得
        max_times_score = Score.objects.filter(
            user=self.request.user,
            question_set=self.question_set
        ).order_by('-times').first()
        
        if max_times_score:
            # 最大のtimesを持つスコアのscoreをインクリメント
            max_times_score.score += 1
            max_times_score.save()
        else:
            # まだスコアが存在しない場合
            return reverse_lazy('ba:questionset_list')
        
    # ログインユーザーの得点を取得
    def get_current_score(self):
        # ユーザーと問題集に関連するスコアオブジェクトのうち、最新のものを取得する
        question_set_id = self.question_set.id
        question_set = QuestionSet.objects.get(pk=question_set_id)
        score = Score.objects.filter(user=self.request.user, question_set=question_set).order_by('-times').first()
        return score
    
    # 解答を終了したときの日時を保存する
    def save_completion_date(self):
        # ユーザーと問題集に関連するスコアオブジェクトのうち、最新のものを取得する
        question_set_id = self.question_set.id
        question_set = QuestionSet.objects.get(pk=question_set_id)
        score = Score.objects.filter(user=self.request.user, question_set=question_set).order_by('-times').first()
        if score:
            score.date = timezone.now()
            score.save()
        
    # 解答した回数をインクリメント    
    def increment_count(self):
        score = self.get_current_score()
        score.count += 1
        score.save()
    
    # 全ての問題に解答したかどうかを判定
    def is_all_questions_answered(self):
        total_questions_count = self.question_set.question_set.count()
        answered_questions_count = self.get_current_score().count
        return total_questions_count == answered_questions_count  
            
    def create_final_score(self):
        # 解答が終了したかどうかの判定
        if self.is_all_questions_answered():
            question_set_id = self.question_set.id
            question_set = QuestionSet.objects.get(pk=question_set_id)
            score = Score.objects.filter(user=self.request.user, question_set=question_set).order_by('-times').first()
            
        
            # 直前の受験回数を取得
            previous_final_score = FinalScore.objects.filter(user=self.request.user, question_set=self.question_set).order_by('-times').first()
            previous_times = previous_final_score.times if previous_final_score else 0
            
            if score:
                # FinalScoreにスコアの内容をコピー
                final_score = FinalScore.objects.create(
                    user=self.request.user,
                    question_set=question_set,
                    score=score.score,
                    times=previous_times+1,
                    date=score.date
                )
                return final_score
            

# スコア結果画面
class ResultView(DetailView):
    model = FinalScore
    template_name = 'ba/ba_result.html'
    context_object_name = 'score'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        score = self.get_object()
        question_set = score.question_set
        answers = Answer.objects.filter(user=self.request.user, question__question_set=question_set)
        
        question_count = score.question_set.question_set.count()
        context['question_count'] = question_count
        
        # 問題ごとの解答結果を格納する辞書を作成
        question_results = {}
        for answer in answers:
            question_text = answer.question.text
            correct_options = [option.text for option in answer.selected_options.filter(is_correct=True)]
            selected_options = [option.text for option in answer.selected_options.all()]
            if set(selected_options) == set(correct_options):
                result = '正解'
            else:
                result = '不正解'
            question_results[question_text] = result

        context['question_results'] = question_results
        #print(question_results)
        
        rate = (score.score / question_count) * 100
        score.rate = rate
        print(rate)
        score.save()
        return context


# スコア結果一覧画面
class ResultListView(ListView):
    model = FinalScore
    template_name = 'ba/ba_result_list.html'
    context_object_name = 'scores'
    
    
# コーヒー豆一覧画面
class BeanListView(ListView):
    model = Bean
    template_name = 'ba/ba_bean_list.html'
    context_object_name = 'beans'


# コーヒー豆詳細画面
class BeanDetailView(DetailView):
    model = Bean
    template_name = 'ba/ba_bean_detail.html'
    context_object_name = 'bean'
    
    
# コーヒー豆検索用ビュー
class BeanSearchView(ListView):
    model = Bean
    template_name = 'ba/ba_bean_list.html'
    context_object_name = 'beans'
    paginate_by = 10

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query.strip():
            # コーヒー名またはスリーレターに一致するコーヒー豆をフィルタリングして返す
            return Bean.objects.filter(name__icontains=query) | Bean.objects.filter(three_letters__icontains=query)
        else:
            # クエリが空白の場合はすべてのコーヒー豆を返す
            return Bean.objects.all()
            
    
    


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
class ManagerQuestionSetListView(LoginRequiredMixin, ListView):
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
class ManagerQuestionDetailView(LoginRequiredMixin, DetailView):
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
    #success_url = reverse_lazy('ba:question_set_list')
    login_url = '/ba/login_manager/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        question = self.get_object()
        options = Option.objects.filter(question=question)
        context['options'] = options
        return context
    
    def get_success_url(self):
        # 問題の詳細画面に遷移するためのURLを取得し、問題のIDを渡す
        return reverse('ba:question_detail', kwargs={'pk': self.object.pk})


# 【管理者】選択肢更新画面
class UpdateOptionView(LoginRequiredMixin, UpdateView):
    model = Option
    template_name = 'ba/ba_manager_update_Option.html'
    form_class = UpdateOptionForm
    #success_url = reverse_lazy('ba:question_set_list')
    login_url = '/ba/login_manager/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        options = self.get_object()
        context['options'] = options
        return context
    
    def get_success_url(self):
        # 問題の詳細画面に遷移するためのURLを取得し、問題のIDを渡す
        return reverse('ba:question_detail', kwargs={'pk': self.object.question.pk})


# 【管理者】問題集削除画面
class DeleteQuestionSetView(LoginRequiredMixin, DeleteView):
    model = QuestionSet
    success_url = reverse_lazy('ba:question_set_list')
    template_name = 'ba/ba_manager_delete_QuestionSet.html'
    login_url = '/ba/login_manager/'


# 【管理者】問題削除画面
class DeleteQuestionView(LoginRequiredMixin, DeleteView):
    model = Question
    template_name = 'ba/ba_manager_delete_Question.html'
    login_url = '/ba/login_manager/'

    def get_queryset(self):
        queryset = super().get_queryset()
        #return queryset.filter(created_by=self.request.user)  # ログインユーザーが作成した問題のみ削除可能
        return queryset

    def get_success_url(self):
        # 問題削除後のリダイレクト先を設定
        return reverse_lazy('ba:question_set_detail', kwargs={'pk': self.object.question_set.id})


# 【管理者】コーヒー豆一覧画面
class ManagerBeanListView(LoginRequiredMixin, ListView):
    model = Bean
    template_name = 'ba/ba_manager_bean_list.html'
    context_object_name = 'beans'
    login_url = '/ba/login_manager/'
    

# 【管理者】コーヒー豆追加画面
class CreateBeanView(LoginRequiredMixin, CreateView):
    model = Bean
    form_class = CreateBeanForm
    template_name = 'ba/ba_manager_create_Bean.html'
    success_url = reverse_lazy('ba:bean_list')
    login_url = '/ba/login_manager/'
    
    def form_valid(self, form):
        # フォームのデータを受け取り、コーヒー豆を作成する
        bean = form.save(commit=False)  # まだ保存はしない
        # form.cleaned_data を使って追加の処理が可能
        bean.save()  # ここで保存する
        return super().form_valid(form)


# 【管理者】コーヒー豆詳細画面
class ManagerBeanDetailView(LoginRequiredMixin, DetailView):
    model = Bean
    template_name = 'ba/ba_manager_Bean_detail.html'
    context_object_name = 'bean'
    login_url = '/ba/login_manager/'
    
    
# 【管理者】コーヒー豆更新画面
class UpdateBeanView(LoginRequiredMixin, UpdateView):
    model = Bean
    form_class = UpdateBeanForm
    template_name = 'ba/ba_manager_update_Bean.html'
    login_url = '/ba/login_manager/'
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['initial'] = {
            'processing': [choice[0] for choice in UpdateBeanForm.PROCESSING_CHOICES if choice[0] in self.object.processing]
        }
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['bean'] = self.get_object()
        return context    

    def get_success_url(self):
        return reverse_lazy('ba:bean_detail', kwargs={'pk': self.object.id})


# 【管理者】コーヒー豆削除画面
class DeleteBeanView(LoginRequiredMixin, DeleteView):
    model = Bean
    template_name = 'ba/ba_manager_delete_Bean.html'
    success_url = reverse_lazy('ba:bean_list')
    login_url = '/ba/login_manager/'



















































    
    
    
    


