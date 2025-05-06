from django.urls import path
from .views import register_views, login_view, logout_user, teacher_list, subject_list_ajax, teacher_profile_creation, teacher_profile, teacher_profile_page, schedule_form_view, teacher_book_list, accept_booking

urlpatterns = [
    path('register/teacher', register_views, name='teacher-register'),
    path('login/teacher', login_view, name='teacher-login'),
    path('logout/', logout_user, name='teacher-logout'),
    path('teachers-list/', teacher_list, name='teachers-list'),
    path('ajax/subjects/', subject_list_ajax, name='subjects-list-ajax'),
    path('create-profile/', teacher_profile_creation, name='teacher-profile-creation'),
    path('profile/', teacher_profile, name='teacher-profile'),
    path('profile/<str:username>/', teacher_profile_page , name='teacher-profile-page'),
    path('teacher/schedule/create', schedule_form_view, name='schedule-form'),
    path('booking-page', teacher_book_list, name='teacher-booking-page'),
    path('booking/<int:booking_id>/accept/', accept_booking, name='accept_booking'),
]
