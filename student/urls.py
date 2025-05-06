from django.urls import path
from .views import student_register, student_profile, student_profile_creation, booking_list, student_edit_profile

urlpatterns = [
    path('register/', student_register, name='student-register'),
    path('profile/', student_profile, name='student-profile'),
    path('profie-creation/' , student_profile_creation, name='student-profile-creation'),
    path('booking-list/', booking_list, name='booking-list'),
    path('edit_profile/', student_edit_profile, name='student-edit-profile')
]
