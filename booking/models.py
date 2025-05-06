from django.db import models
from student.models import Student
from teacher.models import Teacher, ScheduleSlot

class Booking(models.Model):
    
    BOOKING_STATUS_CHOICES = [
        ('pending', 'ожидает'),
        ('confirmed', 'подтверждено'),
        ('cancelled', 'отменено'),
        ('completed', 'завершено'),
    ]
    
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    schedule_slot = models.ForeignKey(ScheduleSlot, on_delete=models.CASCADE, null=True, blank=True)
    booking_date = models.DateTimeField(auto_now_add=True)
    booking_status = models.CharField(choices=BOOKING_STATUS_CHOICES, max_length=15)
    comments = models.TextField(max_length=200, null=True, blank=True)
    price = models.IntegerField()
    
    def __str__(self):
        return f"{self.student} {self.teacher}"


# Create your models here.
