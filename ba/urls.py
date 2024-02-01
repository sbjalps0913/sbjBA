from django.urls import path
from .views import StartView, LoginView, LogoutView, HomeView, RegisterView
from .views import LoginManagerView, HomeManagerView, CreateQuestionSetView, QuestionSetListView


app_name = 'ba'
urlpatterns = [
    # 通常ユーザ
    path('start/', StartView.as_view(), name='start'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('home/', HomeView.as_view(), name='home'),
    
    # 管理者ユーザ
    path('login_manager/', LoginManagerView.as_view(), name='login_manager'),
    path('home_manager/', HomeManagerView.as_view(), name='home_manager'),
    path('create_question_set/', CreateQuestionSetView.as_view(), name='create_question_set'),
    path('question_set_list/', QuestionSetListView.as_view(), name='question_set_list'),
    
]