from django.contrib import admin
from .models import Subject, Teacher, ScheduleSlot, Review
# Register your models here.

admin.site.register(Subject)
admin.site.register(Teacher)
admin.site.register(ScheduleSlot)
admin.site.register(Review)