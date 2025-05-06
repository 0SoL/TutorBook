from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    STUDENT = 'student'
    TEACHER = 'teacher'

    ROLE_CHOICES = [
        (STUDENT, 'Студент'),
        (TEACHER, 'Учитель'),
    ]

    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default=STUDENT)
    phone_number = models.CharField(max_length=20, unique=True, null=True, blank=True)

    def is_teacher(self):
        return self.role == self.TEACHER

    def is_student(self):
        return self.role == self.STUDENT