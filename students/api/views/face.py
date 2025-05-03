# students/api/views/face.py

from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from students.models import Student
from students.face_utils import extract_face_vector

@api_view(['POST'])
@parser_classes([MultiPartParser])  # Cho phép nhận file
def register_face(request):
    student_code = request.data.get('student_code')
    image_file = request.data.get('image')  # Đây là InMemoryUploadedFile

    if not student_code or not image_file:
        return Response({'error': 'Thiếu mã học sinh hoặc ảnh'}, status=400)

    student = get_object_or_404(Student, student_code=student_code)

    try:
        vector = extract_face_vector(image_file.read())  # Đọc file ảnh
        if vector is None:
            return Response({'error': 'Không phát hiện khuôn mặt'}, status=400)

        student.face_vector = vector
        student.save()
        return Response({'message': 'Đăng ký khuôn mặt thành công'})
    except Exception as e:
        return Response({'error': str(e)}, status=500)
