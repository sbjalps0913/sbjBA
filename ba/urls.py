from django.urls import path
from .views import DeleteResultView, QuestionDetailView2, QuestionListView, BeanSearchView, BeanListView, BeanDetailView, ResultView, ResultListView, AnswerQuestionView, QuestionDetailView, StartQuestionView, StartView, LoginView, LogoutView, HomeView, RegisterView, QuestionSetListView
from .views import DeleteQuestionSetView, DeleteQuestionView, UpdateOptionView, UpdateQuestionView, UpdateQuestionSetView, ManagerQuestionDetailView, QuestionSetDetailView, CreateQuestionView, LoginManagerView, HomeManagerView, CreateQuestionSetView, ManagerQuestionSetListView
from .views import ManagerBeanListView, CreateBeanView, ManagerBeanDetailView, UpdateBeanView, DeleteBeanView


app_name = 'ba'
urlpatterns = [
    # 通常ユーザ
    path('start/', StartView.as_view(), name='start'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('home/', HomeView.as_view(), name='home'),
    
    path('question_set/list/', QuestionSetListView.as_view(), name='questionset_list'),
    path('question_set/<int:pk>/start/', StartQuestionView.as_view(), name='start_question'),
    path('question/<int:pk>/detail/', QuestionDetailView.as_view(), name='user_question_detail'),
    path('question/<int:pk>/detail2/', QuestionDetailView2.as_view(), name='user_question_detail2'),
    path('question/<int:pk>/answer/', AnswerQuestionView.as_view(), name='answer_question'),
    path('question/list/', QuestionListView.as_view(), name='question_list'),
    path('result/<int:pk>/', ResultView.as_view(), name='result'),
    path('result/list/', ResultListView.as_view(), name='result_list'),
    path('result/delete/', DeleteResultView.as_view(), name='delete_result'),
    
    path('beans/list/', BeanListView.as_view(), name='user_bean_list'),
    path('beans_detail/<int:pk>/', BeanDetailView.as_view(), name='user_bean_detail'),
    path('beans/search/', BeanSearchView.as_view(), name='bean_search'),
    
    
    # 管理者ユーザ
    path('login_manager/', LoginManagerView.as_view(), name='login_manager'),
    path('home_manager/', HomeManagerView.as_view(), name='home_manager'),
    
    path('create_question_set/', CreateQuestionSetView.as_view(), name='create_question_set'),
    path('question_set_list/', ManagerQuestionSetListView.as_view(), name='question_set_list'),
    path('question_set_detail/<int:pk>/', QuestionSetDetailView.as_view(), name='question_set_detail'),
    path('question_detail/<int:pk>/', ManagerQuestionDetailView.as_view(), name='question_detail'),
    path('question_set/<int:pk>/create_question/', CreateQuestionView.as_view(), name='create_question'),
    
    path('question_set/<int:pk>/update/', UpdateQuestionSetView.as_view(), name='update_question_set'),
    path('question/<int:pk>/update/', UpdateQuestionView.as_view(), name='update_question'),
    path('option/<int:pk>/update/', UpdateOptionView.as_view(), name='update_option'),
    
    path('question/<int:pk>/delete/', DeleteQuestionView.as_view(), name='delete_question'),
    path('question_set/<int:pk>/delete/', DeleteQuestionSetView.as_view(), name='delete_question_set'),

    path('bean/list/', ManagerBeanListView.as_view(), name='bean_list'),
    path('bean/create/', CreateBeanView.as_view(), name='create_bean'),
    path('bean_detail/<int:pk>/', ManagerBeanDetailView.as_view(), name='bean_detail'),
    path('bean/<int:pk>/update/', UpdateBeanView.as_view(), name='update_bean'),
    path('bean/<int:pk>/delete/', DeleteBeanView.as_view(), name='bean_delete'),
    
    
]