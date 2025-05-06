from user.models import CustomUser
from .models import Booking
from django import forms
from teacher.models import ScheduleSlot
from django.utils import timezone
        

class BookingCreationForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ('comments', 'schedule_slot',)
        
    def __init__(self, *args, **kwargs):
        teacher = kwargs.pop('teacher', None)
        super().__init__(*args, **kwargs)
        if teacher:
            today = timezone.now().date()
            self.fields['schedule_slot'].queryset = ScheduleSlot.objects.filter(
                teacher=teacher,
                is_booked=False,
                date__gte=today  # вот это и чистит старые даты!
            ).order_by('date', 'time')