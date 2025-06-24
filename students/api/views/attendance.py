from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.utils.timezone import now
from datetime import datetime, timedelta
from students.models import Student, Schedule, Attendance
from students.face_utils import extract_face_vector
import numpy as np
import pytz


@api_view(['POST'])
def face_checkin_api(request):
    import requests
    from django.utils.timezone import now
    from datetime import datetime, timedelta
    import numpy as np

    student_code = request.data.get("student_code")
    image_url = request.data.get('image_url')
    print(student_code)
    print(image_url)

    if not student_code or not image_url:
        return Response({"error": "Thiếu mã học sinh hoặc ảnh"}, status=400)

    student = Student.objects.filter(student_code=student_code).first()
    if not student:
        return Response({"error": "Không tìm thấy học sinh"}, status=404)

    if not student.face_vector:
        return Response({"error": "Học sinh chưa đăng ký khuôn mặt"}, status=400)

    # Tải ảnh từ URL
    image_response = requests.get(image_url)
    if image_response.status_code != 200:
        return Response({'error': 'Không tải được ảnh từ URL'}, status=400)

    image_bytes = image_response.content
    from students.face_utils import extract_face_vector
    input_vector = extract_face_vector(image_bytes)

    if input_vector is None:
        return Response({"error": "Không phát hiện khuôn mặt"}, status=400)

    def cosine_similarity(v1, v2):
        return float(np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2)))

    similarity = cosine_similarity(student.face_vector, input_vector)
    if similarity < 0.5:
        return Response({"error": "Khuôn mặt không trùng khớp"}, status=400)

    today = now().date()
    weekday = today.isoweekday() + 1
    print(weekday)
    from students.models import Schedule, Attendance
    schedules = Schedule.objects.filter(class_obj=student.class_obj, day_of_week=weekday)

    if not schedules.exists():
        return Response({"error": "Hôm nay không có lịch học"}, status=400)
    vietnam_tz = pytz.timezone("Asia/Ho_Chi_Minh")
    current_time = datetime.now(vietnam_tz).time()

    for schedule in schedules:
        start = schedule.start_time
        limit = (datetime.combine(datetime.today(), start) + timedelta(minutes=15)).time()
        print(start)
        print(limit)
        print(current_time)
        if start <= current_time <= limit:
            status = "on_time"
        elif current_time > limit:
            status = "late"
        else:
            continue

        attendance, created = Attendance.objects.get_or_create(
            student=student, date=today,
            defaults={"status": status}
        )

        if not created:
            return Response({"message": "Đã điểm danh trước đó", "status": attendance.status})
        return Response({"message": "Điểm danh thành công", "status": status})

    return Response({"error": "Không nằm trong thời gian điểm danh"}, status=400)
