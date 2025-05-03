from datetime import datetime
from rest_framework.decorators import api_view
from rest_framework.response import Response
from students.models import Student, Homework, HomeworkScore

@api_view(['GET'])
def homework_summary_view(request, student_code):
    # Nếu không truyền month -> dùng tháng hiện tại
    month = request.GET.get("month", datetime.now().strftime("%m/%Y"))

    try:
        student = Student.objects.get(student_code=student_code)
    except Student.DoesNotExist:
        return Response({"error": "Student not found"}, status=404)

    try:
        m, y = map(int, month.split("/"))
    except:
        return Response({"error": "Invalid month format. Use MM/YYYY"}, status=400)

    # Lọc bài tập theo lớp và tháng
    homeworks = Homework.objects.filter(
        class_obj=student.class_obj,
        date__month=m,
        date__year=y,
        type="btvn"
    ).order_by("date")

    data = []
    for hw in homeworks:
        score_obj = HomeworkScore.objects.filter(student=student, homework=hw).first()
        data.append({
            "date": hw.date.strftime("%d/%m"),
            "score": score_obj.score if score_obj else None,
            "link": hw.link or None
        })

    return Response(data)
