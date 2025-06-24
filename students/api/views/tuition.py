from datetime import datetime
import pytz
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from students.models import TuitionRecord, Student

# Hàm hỗ trợ lấy giờ VN
def now_vietnam():
    vn_tz = pytz.timezone("Asia/Ho_Chi_Minh")
    return datetime.now(vn_tz)

@api_view(['GET'])
def get_tuition_info(request, student_id):
    # Lấy tháng năm (theo giờ VN)
    month = request.GET.get("month", now_vietnam().strftime("%m/%Y"))

    record = TuitionRecord.objects.filter(student__id=student_id, month=month).first()

    if not record:
        return Response({
            "student_id": student_id,
            "month": month,
            "status": "chưa đóng",
            "record": None,
            "submitted_at": None,
            "approved_at": None,
            "amount": 1200000
        })

    return Response({
        "student_id": student_id,
        "month": month,
        "status": record.status,
        "proof_image_url": record.proof_image_url if record.proof_image_url else None,
        "submitted_at": record.submitted_at,
        "approved_at": record.approved_at,
        "amount": record.amount
    })

@api_view(['POST'])
def confirm_tuition_payment(request):
    student_code = request.data.get('student_code')
    # Tháng năm hiện tại (giờ VN)
    month = now_vietnam().strftime("%m/%Y")
    image = request.data.get('proof_image_url')

    print(student_code)
    print(image)
    print(month)

    if not all([student_code, month, image]):
        return Response({"error": "Thiếu thông tin."}, status=status.HTTP_400_BAD_REQUEST)

    student = Student.objects.filter(student_code=student_code).first()
    if not student:
        return Response({"error": "Không tìm thấy học sinh."}, status=status.HTTP_404_NOT_FOUND)

    record, created = TuitionRecord.objects.get_or_create(student=student, month=month)

    if created:
        record.amount = 1200000
    record.proof_image_url = image
    record.status = 'pending'
    record.submitted_at = now_vietnam()  # Giờ VN
    print(record.amount)
    record.save()

    return Response({"message": "Gửi minh chứng thành công."}, status=status.HTTP_200_OK)
