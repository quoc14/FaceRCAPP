from rest_framework.decorators import api_view
from rest_framework.response import Response
from datetime import datetime
from django.utils import timezone
import pytz
from students.models import Student, Schedule
from django.shortcuts import get_object_or_404

@api_view(['GET'])
def schedule_today(request, student_code):
    # Lấy học sinh
    student = get_object_or_404(Student, student_code=student_code)

    # Lấy múi giờ Việt Nam
    vietnam_tz = pytz.timezone("Asia/Ho_Chi_Minh")
    now_vn = datetime.now(vietnam_tz)
    weekday = now_vn.isoweekday() + 1  # Vì isoweekday: Monday=1

    # Lấy lịch học hôm nay
    schedule = Schedule.objects.filter(class_obj=student.class_obj, day_of_week=weekday).first()
    print(f"Today (VN): {now_vn}, weekday={weekday}")

    if not schedule:
        return Response({'schedule': None})

    # Định dạng ngày và giờ
    formatted_date = now_vn.strftime("%d/%m/%Y")
    formatted_time = schedule.start_time.strftime("%Hh%Mp")

    # Lấy phòng
    location = f"Room {student.class_obj.room}" if student.class_obj.room else "Phòng chưa cập nhật"

    return Response({
        'schedule': {
            'subject': schedule.class_obj.name,
            'date': formatted_date,
            'time': formatted_time,
            'location': location
        }
    })
