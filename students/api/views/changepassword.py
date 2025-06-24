from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from students.models import Student
from django.contrib.auth.hashers import check_password, make_password

@api_view(['POST'])
def change_password(request):
    student_code = request.data.get('student_code')
    old_password = request.data.get('old_password')
    new_password = request.data.get('new_password')

    if not student_code or not old_password or not new_password:
        return Response({'error': 'Vui lòng nhập đầy đủ thông tin'},
                        status=status.HTTP_400_BAD_REQUEST)

    student = Student.objects.filter(student_code=student_code).first()
    if not student:
        return Response({'error': 'Không tìm thấy học sinh'},
                        status=status.HTTP_404_NOT_FOUND)

    if not check_password(old_password, student.password):
        return Response({'error': 'Mật khẩu cũ không đúng'},
                        status=status.HTTP_401_UNAUTHORIZED)

    student.password = make_password(new_password)
    student.save()

    return Response({'message': 'Đổi mật khẩu thành công!'})
