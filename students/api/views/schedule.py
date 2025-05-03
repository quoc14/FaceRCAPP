from rest_framework.decorators import api_view
from rest_framework.response import Response
from students.models import Schedule
from datetime import datetime

@api_view(['GET'])
def schedule_today(request, class_id):
    # Lấy ngày từ query param hoặc dùng hôm nay
    date_str = request.GET.get('date', datetime.now().strftime("%Y-%m-%d"))
    try:
        date = datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        return Response({"error": "Ngày không hợp lệ. Định dạng đúng: YYYY-MM-DD"}, status=400)

    # Django weekday: 0=Mon, 6=Sun. Hệ thống: 2=T2, ..., 8=CN
    day_of_week = date.weekday() + 2

    schedules = Schedule.objects.filter(class_obj__id=class_id, day_of_week=day_of_week)
    data = []
    for schedule in schedules:
        data.append({
            "day": f"T{day_of_week}" if day_of_week <= 7 else "CN",
            "start_time": schedule.start_time.strftime("%H:%M"),
            "end_time": schedule.end_time.strftime("%H:%M"),
            "room": schedule.class_obj.room
            
        })

    return Response(data)
