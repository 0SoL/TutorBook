from django.urls import path 
from . import views


urlpatterns = [
    path('chat/<int:room_id>/', views.chat_room, name='chat_room'),
    path('start_chat/<int:teacher_id>/', views.start_chat, name='start_chat'),
    path('dialogs/', views.dialog_list, name='dialogs'),
    path('teacher/dialogs/', views.teacher_dialogs_list, name='teacher_dialogs_list'),
]
