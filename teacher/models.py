from django.db import models
from django.contrib.auth.models import User
from django.conf import settings 

class Subject(models.Model):
    name = models.CharField(max_length=30)
    
    def __str__(self):
        return f'{self.name}'

class Teacher(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    bio = models.TextField()
    subject = models.ManyToManyField(Subject)
    price_per_hous = models.IntegerField()
    work_experience = models.IntegerField()
    avatar = models.ImageField(upload_to='avatars', default='avatar_threshold.png')
    
    def __str__(self):
        return f'{self.user}'

class ScheduleSlot(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    is_booked = models.BooleanField(default=False)
    
    def __str__(self):
        return f'{self.date}, {self.time}'
    
# Create your models here.
