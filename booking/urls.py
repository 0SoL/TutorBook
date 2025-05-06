from django.urls import path
from .views import lesson_booking, get_available_slots

urlpatterns = [
    path('book-lesson/<str:username>/', lesson_booking, name='lesson-booking'),
    path('get-slots/<int:teacher_id>/<str:selected_date>/', get_available_slots, name='get-slots'),
]
