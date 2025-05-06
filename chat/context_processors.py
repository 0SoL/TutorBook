from .models import ChatRoom
from student.models import Student
from teacher.models import Teacher

def dialogs_processor(request):
    if not request.user.is_authenticated:
        return {}

    dialogs = []

    try:
        student = Student.objects.get(user=request.user)
        dialogs = ChatRoom.objects.filter(student=student).order_by('-id')
    except Student.DoesNotExist:
        try:
            teacher = Teacher.objects.get(user=request.user)
            dialogs = ChatRoom.objects.filter(teacher=teacher).order_by('-id')
        except Teacher.DoesNotExist:
            dialogs = []

    return {'navbar_dialogs': dialogs}