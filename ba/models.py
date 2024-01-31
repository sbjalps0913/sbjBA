from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Question(models.Model):
    question_text = models.CharField(max_length=255)
    # 他にも必要なフィールドを追加


class Option(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    option_text = models.CharField(max_length=100)
    is_correct = models.BooleanField(default=False)


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_master = models.BooleanField(default=False)
    
    def __str__(self):
        return self.user.username