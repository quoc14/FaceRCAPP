from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from students.models import Student
from students.api.serializers import StudentProfileSerializer
from django.shortcuts import get_object_or_404

@api_view(['GET'])
def student_profile(request, student_code):
    student = get_object_or_404(Student, student_code=student_code)
    serializer = StudentProfileSerializer(student)
    return Response(serializer.data)
