from datetime import date, timedelta
from teacher.models import ScheduleSlot
import datetime

def generate_schedule_slot(teacher, start_time, end_time, interval, work_days):
    today = date.today()
    for i in range(14):
        current_date = today + timedelta(days=i)
        
        weekday_map = {'mon': 0, 'tue': 1, 'wed': 2, 'thu': 3, 'fri': 4, 'sat': 5, 'sun': 6}
        work_day_indexes = [weekday_map[day] for day in work_days]
        
        if current_date.weekday() not in work_day_indexes:
            continue
        
        current_time = start_time
        while current_time <= end_time:
            if not ScheduleSlot.objects.filter(
                    teacher=teacher,
                    date=current_date,
                    time=current_time).exists():
                
                ScheduleSlot.objects.create(
                    teacher = teacher,
                    date = current_date,
                    time = current_time,
                    is_booked = False
                )
                
            slot_datetime = datetime.datetime.combine(current_date, current_time)
            slot_datetime += timedelta(minutes=interval + 10)
            current_time = slot_datetime.time()