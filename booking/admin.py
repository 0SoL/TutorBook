from django.contrib import admin
from .models import Booking
# Register your models here.
class BookingAdmin(admin.ModelAdmin):
    list_display = ('student', 'teacher', 'booking_date', 'booking_status', 'comments', 'price')
    
admin.site.register(Booking, BookingAdmin)