from django.shortcuts import render, get_object_or_404, redirect
from .models import ChatRoom, Message
from teacher.models import Teacher
from student.models import Student
from django.db.models import Max

# Create your views here.
def chat_room(request, room_id):
    # Получаем комнату по ID
    room = get_object_or_404(ChatRoom, id=room_id)

    # Проверка, что пользователь имеет право тут быть
    if request.user != room.student.user and request.user != room.teacher.user:
        return render(request, '403.html')  # Страница ошибки доступа

    # Все сообщения этой комнаты
    messages = room.messages.order_by('timestamp')

    context = {
        'room': room,
        'messages': messages,
    }
    return render(request, 'chat/lobby.html', context)

def start_chat(request, teacher_id):
    teacher = get_object_or_404(Teacher, id=teacher_id)

    
    student = get_object_or_404(Student, user=request.user)

    
    chat_room, created = ChatRoom.objects.get_or_create(
        student=student,
        teacher=teacher
    )

    return redirect('chat_room', room_id=chat_room.id)

def dialog_list(request):
    student = get_object_or_404(Student, user=request.user)
    
    chatrooms = ChatRoom.objects.filter(student=student)
    
    chatrooms = chatrooms.annotate(
        last_message_time=Max('messages__timestamp')
    ).order_by('-last_message_time')
    
    context = {'chatrooms' : chatrooms}
    
    return render(request, 'chat/dialogs.html', context)

def teacher_dialogs_list(request):
    # Получаем учителя
    teacher = get_object_or_404(Teacher, user=request.user)

    # Ищем все комнаты учителя
    chatrooms = ChatRoom.objects.filter(teacher=teacher)

    chatrooms = chatrooms.annotate(
        last_message_time=Max('messages__timestamp')
    ).order_by('-last_message_time')

    context = {
        'chatrooms': chatrooms,
    }
    return render(request, 'chat/teacher_dialogs_list.html', context)