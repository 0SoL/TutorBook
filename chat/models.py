from django.db import models
from student.models import Student
from teacher.models import Teacher
from user.models import CustomUser



class ChatRoom(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    
class Message(models.Model):
    chatroom = models.ForeignKey(ChatRoom, on_delete=models.CASCADE,related_name='messages' )
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
# Create your models here.
