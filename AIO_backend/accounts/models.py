from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    email = models.EmailField(unique=True)
    gender = models.CharField(max_length=10, blank=True, null=True)     # "male", "female"
    age_group = models.CharField(max_length=10, blank=True, null=True)  # "10s", "20s", etc.

    nickname = models.CharField(max_length=50, blank=True, null=True)
    profile_image = models.ImageField(upload_to='profiles/', blank=True, null=True)
    
    # 추가: 챗봇 이미지 필드
    chatbot_image = models.ImageField(upload_to='chatbots/', blank=True, null=True)

    def __str__(self):
        return self.email