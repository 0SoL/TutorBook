from django.contrib.auth.forms import UserCreationForm
from user.models import CustomUser
from .models import Teacher
from django import forms

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2')  # можно не показывать role, если задаёшь вручную
        

class TeacherProfileForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = ('bio', 'subject', 'price_per_hous', 'work_experience', 'avatar')
        
        
class ScheduleGenerationForm(forms.Form):
    start_time = forms.TimeField(label="Время начала", widget=forms.TimeInput(format='%H:%M', attrs={'type': 'time'}))
    end_time = forms.TimeField(label="Время окончания", widget=forms.TimeInput(format='%H:%M', attrs={'type': 'time'}))
    
    INTERVAL_CHOICES = [
        (50, '50 минут'),
    ]
    interval = forms.ChoiceField(choices=INTERVAL_CHOICES, label="Интервал")

    WEEKDAYS = [
        ('mon', 'Понедельник'),
        ('tue', 'Вторник'),
        ('wed', 'Среда'),
        ('thu', 'Четверг'),
        ('fri', 'Пятница'),
        ('sat', 'Суббота'),
        ('sun', 'Воскресенье'),
    ]
    work_days = forms.MultipleChoiceField(
        choices=WEEKDAYS,
        widget=forms.CheckboxSelectMultiple,
        label="Рабочие дни"
    )