from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


# Create your models here.

# 問題集
class QuestionSet(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()    # 問題集の説明
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)     # 問題を作成したユーザ
    created_at = models.DateTimeField(auto_now_add=True)    # 問題集の作成日時

    def __str__(self):
        return self.title

# 個々の問題を表すモデル
class Question(models.Model):
    question_set = models.ForeignKey(QuestionSet, on_delete=models.CASCADE)     # 属する問題集
    text = models.TextField()
    explanation = models.TextField(blank=True, null=True)   # 解説
    
    def __str__(self):
        return self.text

# 選択肢
class Option(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)    # 属する問題
    text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)     # 正解か否か
    
    def __str__(self):
        return self.text


# ユーザモデル
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='userprofile')
    is_manager = models.BooleanField(default=False)
    
    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()
    

# スコア
class Score(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question_set = models.ForeignKey(QuestionSet, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)
    times = models.IntegerField(default=0)  # 問題集を解いた回数
    date = models.DateTimeField(auto_now_add=True)  # 解答終了日時
    count = models.IntegerField(default=0)  # 解答した問題数

    def __str__(self):
        return f"{self.user.username}'s score for {self.question_set}:{self.times}回目 スコア:{self.score} (受験日:{self.date})"


# 最終スコア
class FinalScore(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question_set = models.ForeignKey(QuestionSet, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)
    times = models.IntegerField(default=0)  # 問題集を解いた回数
    date = models.DateTimeField(auto_now_add=True)  # 解答終了日時

    def __str__(self):
        return f"{self.user.username}'s score for {self.question_set}:{self.times}回目 [{self.score}] 受験日{self.date}"


# コーヒー豆
class Bean(models.Model):
    name = models.CharField(max_length=20)
    three_letters = models.CharField(max_length=3)
    roast = models.IntegerField()  # ローストレベル
    flavor = models.CharField(max_length=50)   # 風味
    acidity = models.CharField(max_length=100)  # 酸味
    body = models.CharField(max_length=100)     # コク
    processing = models.CharField(max_length=100)   # 加工法
    region = models.CharField(max_length=100)   # 地域
    complementary = models.CharField(max_length=50)    # 相性の良い風味

    def __str__(self):
        return self.name    












