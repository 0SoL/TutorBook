from .models import Student
from teacher.models import Teacher

def user_profile_context(request):
    student_profile = None
    teacher_profile = None

    if request.user.is_authenticated:
        try:
            student_profile = Student.objects.get(user=request.user)
        except Student.DoesNotExist:
            pass
        
        try:
            teacher_profile = Teacher.objects.get(user=request.user)
        except Teacher.DoesNotExist:
            pass

    return {
        'student_profile': student_profile,
        'teacher_profile': teacher_profile,
    }