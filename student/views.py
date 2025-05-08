from django.shortcuts import render, redirect, get_object_or_404
from .forms import CustomUserCreationForm
from django.contrib.auth import logout, login, authenticate
from django.contrib import messages
from .models import Student
from .forms import StudentProfileCreationForm, StudentEditProfileForm, StudentEditUserForm, ReviewForm
from booking.models import Booking
from teacher.models import Teacher, Review
from django.http import HttpResponse



# Create your views here.
def student_register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.role = 'student'
            user.save()
            login(request, user)
            messages.success(request, ('Вы успешно зарегистрировались как ученик!'))
            return redirect('student-profile-creation')
    else:
        form = CustomUserCreationForm()
    
    context = {'form': form}

    return render(request, "student/register.html" , context)


def student_profile(request):
    student_user = request.user
    student = get_object_or_404(Student, user=student_user)
    
    context = {'student' : student,
               'student_user' : student_user
               }
    
    return render(request, 'student/student_profile.html', context)


def student_profile_creation(request):
    if request.user.role != 'student':
        return redirect('home')
    
    try:
        profile = request.user.student
    except Student.DoesNotExist:
        profile = None
        
    if request.method == 'POST':
        form = StudentProfileCreationForm(request.POST, request.FILES , instance=profile)
        if form.is_valid():
            student = form.save(commit=False)
            student.user = request.user
            student.save()
            form.save_m2m()
            messages.success(request, 'Профиль успешно обновлен!')
            return redirect('home')
    else:
        form = StudentProfileCreationForm
        
    context = {'form' : form}
    
    return render(request, 'student/student_profile_edit.html', context)

def student_edit_profile(request):
    user = request.user
    student = request.user.student
    
    if request.method == 'POST':
        user_form = StudentEditUserForm(request.POST, instance=user)
        student_form = StudentEditProfileForm(request.POST, request.FILES, instance=student)
        
        if user_form.is_valid() and student_form.is_valid():
            user_form.save()
            student_form.save()
            return redirect('student_profile')
        
    else:
        user_form = StudentEditUserForm(instance=user)
        student_form = StudentEditProfileForm(instance=student)
        
    context = {
        'user_form' : user_form,
        'student_form' : student_form,
        'student' : student
    }
        
    return render(request, 'student/student_edit_profile.html', context)
        

def booking_list(request):
    student = request.user.student
    if request.user.role != 'student':
        return redirect('home')
    
    booking = Booking.objects.filter(
        student = student,
        
    )
    
    context = {'booking' : booking}
    
    return render(request, 'student/booking_list.html' , context)


def review_form(request, teacher_id):
    student = request.user.student
    teacher = get_object_or_404(Teacher, id=teacher_id)
    
    # if Review.objects.filter(teacher=teacher, student=student).exists():
    #     return HttpResponse("Вы уже оставляли отзыв.")
    
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        
        if form.is_valid():
            review = form.save(commit=False)
            review.teacher = teacher
            review.student = student
            review.save()
            return redirect('booking-list')
    else:
        form = ReviewForm()
    
    return render(request, 'student/review.html', {'form' : form, 'teacher' : teacher})
        