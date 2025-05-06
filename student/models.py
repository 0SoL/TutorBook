from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

class Student(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='static/images/avatars', default='static/images/avatar_threshold.png')

    
    def __str__(self):
        return f'{self.user}'
# Create your models here.
