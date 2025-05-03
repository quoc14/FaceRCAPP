from students.models import Class, Student, TuitionRecord
from datetime import datetime

# Tạo lớp mới (nếu cần)
new_class, _ = Class.objects.get_or_create(
    name="8C1",
    grade=8,
    level="C1",
    room="P203"
)

# Tạo học sinh mới
new_student = Student.objects.create(
    student_code="TDT259999",
    name="Nguyễn Văn Mới",
    class_obj=new_class,
    parent_name="Nguyễn Văn Bố",
    parent_phone="0987654321",
    student_phone="0912345678"
)

# Tạo bản ghi học phí chưa duyệt
TuitionRecord.objects.create(
    student=new_student,
    month="04/2025",
    amount=1000000,
    proof_url="https://via.placeholder.com/200",  # Có thể cập nhật sau
    submitted_at=datetime.now(),
    status='pending'
)

student2 = Student.objects.create(
    student_code="TDT259998",
    name="Trần Thị Chưa Đóng",
    class_obj=new_class,
    parent_name="Trần Văn Bố",
    parent_phone="0987888888",
    student_phone="0911222333"
)
