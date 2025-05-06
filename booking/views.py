from django.shortcuts import render, get_object_or_404, redirect
from .forms import BookingCreationForm
from teacher.models import Teacher
from student.models import Student
from .models import ScheduleSlot
from django.http import JsonResponse
from datetime import date

# Create your views here.
def lesson_booking(request, username):
    teacher = get_object_or_404(Teacher, user__username=username)
    student = get_object_or_404(Student, user=request.user)
    if request.method == 'POST':
        form = BookingCreationForm(request.POST, teacher=teacher)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.teacher = teacher
            booking.student = student
            booking.booking_status = 'pending'
            booking.price = teacher.price_per_hous
            booking.save()
            booking.schedule_slot.is_booked = True
            booking.schedule_slot.save()
            return redirect('home')
    else:
        form = BookingCreationForm(teacher=teacher)
        
    context = {'form' : form, 'teacher' : teacher}
    return render(request, 'booking/book_lesson.html' , context)


def get_available_slots(request, teacher_id, selected_date):
    slots = ScheduleSlot.objects.filter(
        teacher_id=teacher_id,
        date=selected_date,
        is_booked=False
    ).order_by('time')
    
    data = [{'id': s.id, 'time': s.time.strftime('%H:%M')} for s in slots]
    return JsonResponse(data, safe=False)
            