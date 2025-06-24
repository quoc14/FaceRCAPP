# students/api/views/face.py
import requests
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from students.models import Student
from students.face_utils import extract_face_vector
import os
@api_view(['POST'])
def register_face(request):
    student_code = request.data.get('student_code')
    image_url = request.data.get('image_url')

    if not student_code or not image_url:
        return Response({'error': 'Thiếu mã học sinh hoặc URL ảnh'}, status=400)

    student = get_object_or_404(Student, student_code=student_code)

    try:
        print(student_code)
        # Tải ảnh từ URL Firebase
        image_response = requests.get(image_url)
        print(image_url)
        if image_response.status_code != 200:
            return Response({'error': 'Không tải được ảnh từ URL'}, status=400)

        image_bytes = image_response.content
        #folder = "debug_faces"
        #os.makedirs(folder, exist_ok=True)
        #filename = f"{folder}/{student_code}.jpg"
        #with open(filename, "wb") as f:
         #   f.write(image_bytes)
        #print(f">> Ảnh đã được lưu tại: {filename}")
        vector = extract_face_vector(image_bytes)

        if vector is None:
            return Response({'error': 'Không phát hiện khuôn mặt'}, status=400)

        # Lưu URL và vector vào model
        student.face_vector = vector
        student.face_image_url = image_url
        student.save()

        return Response({'message': 'Đăng ký khuôn mặt thành công', 'image_url': image_url})
    except Exception as e:
        return Response({'error': str(e)}, status=500)
