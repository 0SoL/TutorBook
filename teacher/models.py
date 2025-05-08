from django.db import models
from django.contrib.auth.models import User
from student.models import Student
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
    education = models.CharField(max_length=255, verbose_name="Образование", blank=True)
    video_intro = models.URLField(blank=True, null=True) 
    languages = models.CharField(max_length=255, blank=True, verbose_name="Языки преподавания")
    rating = models.FloatField(default=0.0, null=True, blank=True)
    review_count = models.PositiveIntegerField(default=0, null=True, blank=True)
    
    def __str__(self):
        return f'{self.user}'

class ScheduleSlot(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    is_booked = models.BooleanField(default=False)
    
    def __str__(self):
        return f'{self.date}, {self.time}'


class Review(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='reviews')
    student = models.ForeignKey(Student, on_delete=models.SET_NULL, null=True, blank=True)
    rating = models.PositiveSmallIntegerField(choices=[(i, str(i)) for i in range(1, 6)])
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.teacher} - {self.rating}⭐"
# Create your models here.
