from django.contrib.auth.forms import UserCreationForm
from user.models import CustomUser
from .models import Student
from django import forms
from django.contrib.auth import get_user_model
from django.forms.widgets import ClearableFileInput
from teacher.models import Review

User = get_user_model()


class NoLabelFileInput(ClearableFileInput):
    template_name = 'student/widgets/plain_file_input.html'

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2')  # можно не показывать role, если задаёшь вручную
        
        
class StudentProfileCreationForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ('avatar',)
        
        
class StudentEditProfileForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ('avatar',)
        widgets = {
            'avatar': NoLabelFileInput(attrs={
                'id': 'custom-avatar',
                'style': 'display: none;',
            }),
        }

        

class StudentEditUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('phone_number',)


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ('rating', 'comment',)
        widgets = {
            'rating': forms.RadioSelect(attrs={'class': 'star-rating'}),
            'comment': forms.Textarea(attrs={'placeholder': 'Ваш отзыв...'}),
        }