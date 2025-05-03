from rest_framework.decorators import api_view
from rest_framework.response import Response
from datetime import datetime
import calendar
from students.models import MonthlySummary, Homework, HomeworkScore, Student
from django.shortcuts import get_object_or_404

@api_view(['GET'])
def monthly_summary_view(request, student_id):
    month_str = request.GET.get('month', datetime.now().strftime('%m/%Y'))
    try:
        m, y = map(int, month_str.split("/"))
        start_date = datetime(y, m, 1).date()
        end_date = datetime(y, m, calendar.monthrange(y, m)[1]).date()
    except:
        return Response({"error": "Invalid month format"}, status=400)

    summary = MonthlySummary.objects.filter(student__id=student_id, month=month_str).first()
    if not summary:
        return Response({"error": "No summary found"}, status=404)
    student = get_object_or_404(Student, id=student_id)
    # Tính điểm BTVN
    homeworks = Homework.objects.filter(class_obj=summary.student.class_obj, type='btvn', date__range=(start_date, end_date))
    scores = HomeworkScore.objects.filter(student__id=student_id, homework__in=homeworks).values_list('score', flat=True)
    btvn_avg = round(sum(scores) / len(scores), 2) if scores else 0

    return Response({
        "student_name": student.name,
        "month": summary.month,
        "btvn_avg": btvn_avg,
        "ktt_score": summary.ktt_score,
        "voucher_score": summary.voucher_score,
        "diligence_score": summary.diligence_score,
        "final_score": summary.final_score,
    })
