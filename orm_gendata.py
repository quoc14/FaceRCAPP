from students.models import Student
from django.contrib.auth.hashers import make_password

students = Student.objects.filter(password__isnull=True) | Student.objects.filter(password='')

for s in students:
    s.password = make_password("123456")
    s.save()

print(f"Đã hash mật khẩu mặc định cho {students.count()} học sinh.")
