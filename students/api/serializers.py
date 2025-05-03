from rest_framework import serializers
from students.models import Student, Class

class ClassSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Class
        fields = ['name', 'grade', 'level']

class StudentProfileSerializer(serializers.ModelSerializer):
    class_obj = ClassSimpleSerializer()

    class Meta:
        model = Student
        fields = ['id', 'student_code', 'name', 'parent_name', 'parent_phone', 'student_phone', 'class_obj']
