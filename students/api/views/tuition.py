from datetime import datetime
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from students.models import TuitionRecord, Student

@api_view(['GET'])
def get_tuition_info(request, student_id):
    month = request.GET.get("month", datetime.now().strftime("%m/%Y"))

    record = TuitionRecord.objects.filter(student__id=student_id, month=month).first()

    if not record:
        return Response({
            "student_id": student_id,
            "month": month,
            "status": "chưa đóng",
            "record": None,
            "submitted_at": None,
            "approved_at": None,
            "amount": 0
        })

    return Response({
        "student_id": student_id,
        "month": month,
        "status": record.status,
        "proof_image": record.proof_url if record.proof_url else None,
        "submitted_at": record.submitted_at,
        "approved_at": record.approved_at,
        "amount": record.amount
    })

@api_view(['POST'])
def confirm_tuition_payment(request):
    student_code = request.data.get('student_code')
    month = datetime.now().strftime("%m/%Y")
    image = request.FILES.get('proof_image')

    if not all([student_code, month, image]):
        return Response({"error": "Thiếu thông tin."}, status=status.HTTP_400_BAD_REQUEST)

    student = Student.objects.filter(student_code=student_code).first()
    if not student:
        return Response({"error": "Không tìm thấy học sinh."}, status=status.HTTP_404_NOT_FOUND)

    record, _ = TuitionRecord.objects.get_or_create(student=student, month=month)
    record.proof_image = image
    record.status = 'pending'
    record.submitted_at = datetime.now()
    record.save()

    return Response({"message": "Gửi minh chứng thành công."}, status=status.HTTP_200_OK)