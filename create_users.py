# create_users.py
import os
import django

# Thiết lập môi trường Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "math_center_api.settings")  # Thay math_center_api bằng tên settings thực tế nếu khác
django.setup()

from django.contrib.auth.models import User

# Tạo user admin
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser(username='admin', email='admin@example.com', password='admin')
    print("✅ Đã tạo user admin (admin/admin)")

# Tạo user teacher
if not User.objects.filter(username='teacher').exists():
    teacher = User.objects.create_user(username='teacher', email='teacher@example.com', password='teacher')
    teacher.is_staff = True
    teacher.save()
    print("✅ Đã tạo user teacher (teacher/teacher)")
