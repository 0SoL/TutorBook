from django.shortcuts import render, redirect, get_object_or_404
from django.core.serializers import serialize
from django.http import HttpResponse
from django.http import JsonResponse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import logout, login, authenticate
from django.contrib import messages
from .models import Teacher, Subject, ScheduleSlot, Review
from .forms import CustomUserCreationForm, TeacherProfileForm, ScheduleGenerationForm
from user.models import CustomUser
from .services.generate_schedule_slot import generate_schedule_slot
from datetime import timedelta
from django.utils import timezone
from collections import defaultdict
from booking.models import Booking


def register_views(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.role = 'teacher'
            user.save()
            login(request, user)
            messages.success(request, ('Вы успешно зарегестрировались'))
            return redirect('teacher-profile-creation')
    else:
        form = CustomUserCreationForm()
    
    context = {'form': form}

    return render(request, "teacher/register.html" , context)

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request,user)
            messages.success(request, ('Вы успешно зашли'))
            return redirect('teachers-list')
        else:
            messages.error(request, ("Вы ввели неправильные данные"))
            return redirect('teacher-login')
    else:
        return render(request, 'teacher/login.html', {})
        


def logout_user(request):
    logout(request)
    messages.success(request, ("Вы успешно вышли"))
    return redirect('teachers-list')

def teacher_profile_creation(request):
    if request.user.role != 'teacher':
        return redirect('teachers-list')
    
    try:
        profile = request.user.teacher
    except Teacher.DoesNotExist:
        profile = None
        
    if request.method == 'POST':
        form = TeacherProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            teacher = form.save(commit=False)
            teacher.user = request.user
            teacher.save()
            form.save_m2m()
            messages.success(request, 'Профиль успешно обновлен!')
            return redirect('teachers-list')
    else:
        form = TeacherProfileForm
    
    context = {'form' : form}
    
    return render(request, 'teacher/profile_creation.html', context)

def teacher_list(request):
    teachers = Teacher.objects.all()
    min_price = Teacher.objects.all().order_by('price_per_hous').first().price_per_hous
    max_price = Teacher.objects.all().order_by('-price_per_hous').first().price_per_hous
    
    
    subjects_contains_query = request.GET.get('subject-select')
    price_min = request.GET.get('price_min')
    price_max = request.GET.get('price_max')
    
    if price_min and price_max:
        teachers = teachers.filter(price_per_hous__gte=price_min, price_per_hous__lte=price_max)
    
    if subjects_contains_query != '' and subjects_contains_query is not None:
        teachers = teachers.filter(subject__id=subjects_contains_query)
        
    context = {
        'teachers' : teachers,
        'min_price': min_price,
        'max_price': max_price,
    
    }
    return render(request, 'teacher/teachers_page.html', context)


def subject_list_ajax(request):
    subjects = Subject.objects.all()
    data = [{"id": s.id, "text": s.name} for s in subjects]
    return JsonResponse({"results": data})

def teacher_filter(request):
    qs = Teacher.objects.all()
    subjects_contains_query = request.GET.get('subjects_select')
    print(subjects_contains_query)
    if subjects_contains_query != '' and subjects_contains_query is not None:
        qs = qs.filter(subject__icontains=subjects_contains_query)
    context = {
        'queryset' : qs
    }
    return render(request, 'teacher/teachers_page.html', context) 
    
    
def teacher_profile(request):
    teacher_user = request.user
    teacher_profile = get_object_or_404(Teacher, user=teacher_user)
    # teacher_schedule = ScheduleSlot.objects.filter(teacher=request.user.teacher)
    
    today = timezone.now().date()
    next_week = today + timedelta(days=7)
    
    slots = ScheduleSlot.objects.filter(
        teacher=request.user.teacher,
        date__range=(today, next_week)
    ).order_by('date', 'time')
    
    grouped_schedule = defaultdict(list)
    for slot in slots:
        grouped_schedule[slot.date].append(slot)
    
    context = {'teacher_user' : teacher_user,
               'teacher_profile' : teacher_profile,
               'grouped_schedule' : dict(grouped_schedule),}
    
    return render(request, 'teacher/teacher_profile.html', context)

def teacher_profile_page(request, username):
    teacher_profile = get_object_or_404(Teacher, user__username=username)
    today = timezone.now().date()
    next_week = today + timedelta(days=7)
    reviews = Review.objects.filter(teacher=teacher_profile)
    
    slots = ScheduleSlot.objects.filter(
        teacher=teacher_profile,
        date__range=(today, next_week)
    ).order_by('date', 'time')
    
    grouped_schedule = defaultdict(list)
    for slot in slots:
        grouped_schedule[slot.date].append(slot)
    
    context = {'teacher_profile' : teacher_profile,
               'grouped_schedule' : dict(grouped_schedule),
               'reviews' : reviews}
    
    return render(request, 'teacher/teacher_profile_page.html', context)
    
def schedule_form_view(request):
    if request.method == 'POST':
        form = ScheduleGenerationForm(request.POST)
        if form.is_valid():
            schedule_data = form.cleaned_data
            print(schedule_data['start_time'])
            generate_schedule_slot(
                teacher=request.user.teacher,
                start_time=schedule_data['start_time'],
                end_time=schedule_data['end_time'],
                interval = int(schedule_data['interval']),
                work_days=schedule_data['work_days']
                )
            messages.success(request, 'Вы успешно создали расписание!')
            return redirect('teacher-list')
    else:
        form = ScheduleGenerationForm()
    return render(request, 'teacher/schedule_form.html', {'form' : form})


def teacher_book_list(request):
    teacher = request.user.teacher
    
    booking = Booking.objects.filter(
        teacher = teacher
    )
    
    context = {'booking' : booking}
    
    return render(request, 'teacher/teacher_book_list.html', context)

def accept_booking(request, booking_id):
    if request.method == 'POST':
        booking = get_object_or_404(Booking, id=booking_id)
        booking.booking_status = 'confirmed'
        booking.save()
        return redirect('teacher-booking-page') 
# Create your views here.
