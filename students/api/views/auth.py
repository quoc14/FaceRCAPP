from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from students.models import Student

@api_view(['POST'])
def student_login(request):
    student_code = request.data.get('student_code')
    if not student_code:
        return Response({'error': 'Vui lòng nhập mã học sinh'}, status=status.HTTP_400_BAD_REQUEST)
    student = Student.objects.filter(student_code=student_code).first()

    if student:
        return Response({
            "message": "Đăng nhập thành công",
            "student_id": student.id,
            "name": student.name,
            "class_id": student.class_obj.id,
            "class_name": student.class_obj.name,
            "student_phone": student.student_phone,
            "parent_name": student.parent_name,
            "parent_phone": student.parent_phone
        })
    else:
        return Response({
            "error": "Mã học sinh không đúng"
        }, status=status.HTTP_401_UNAUTHORIZED)
