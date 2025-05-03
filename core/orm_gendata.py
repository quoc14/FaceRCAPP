import uuid
import random
from datetime import datetime, timedelta, time, date

from students.models import (
    Class, Student, Schedule, Homework, HomeworkScore,
    Attendance, Bonus, MonthlyReport
)

# Xóa dữ liệu cũ (nếu muốn reset sạch)
Class.objects.all().delete()
Student.objects.all().delete()
Schedule.objects.all().delete()
Homework.objects.all().delete()
HomeworkScore.objects.all().delete()
Attendance.objects.all().delete()
Bonus.objects.all().delete()
MonthlyReport.objects.all().delete()

# Tạo lớp học
class_8a = Class.objects.create(name="8A", grade=8, level="A1", room="P201")
class_8b = Class.objects.create(name="8B", grade=8, level="B1", room="P202")

# Lịch học
Schedule.objects.create(class_obj=class_8a, day_of_week=2, start_time=time(17, 15), end_time=time(19, 0), slot_name="T2")
Schedule.objects.create(class_obj=class_8a, day_of_week=7, start_time=time(17, 15), end_time=time(19, 0), slot_name="T7")
Schedule.objects.create(class_obj=class_8b, day_of_week=3, start_time=time(17, 30), end_time=time(19, 15), slot_name="T3")
Schedule.objects.create(class_obj=class_8b, day_of_week=6, start_time=time(17, 30), end_time=time(19, 15), slot_name="T6")

def generate_code(index): return f"TDT25{index:04d}"
today = date.today()
month_str = today.strftime("%m/%Y")

names_8a = ["Nguyễn Minh Ánh", "Phạm Gia Hưng", "Trần Lan Anh"]
names_8b = ["Lê Văn Sơn", "Bùi Phương Linh", "Ngô Thị Hòa"]

for i, name in enumerate(names_8a + names_8b):
    idx = i + 1
    cls = class_8a if i < 3 else class_8b
    student = Student.objects.create(
        name=name,
        student_code=generate_code(idx),
        parent_name=f"Phụ huynh {name.split()[-1]}",
        parent_phone=f"09{random.randint(10000000,99999999)}",
        class_obj=cls
    )

    # Điểm danh 3 buổi
    for j in range(3):
        Attendance.objects.create(
            id=uuid.uuid4(),
            student=student,
            date=today - timedelta(days=j*3),
            status=random.choice(["on_time", "late", "absent"])
        )

    # BTVN tuần 1–3
    for w in range(1, 4):
        hw = Homework.objects.create(
            class_obj=cls,
            title=f"Tuần {w}",
            type="btvn",
            week_number=w,
            weight=1,
            due_date=today - timedelta(days=7 * w)
        )
        HomeworkScore.objects.create(student=student, homework=hw, score=random.uniform(16, 20))

    # Kiểm tra tháng
    ktt = Homework.objects.create(
        class_obj=cls,
        title="KTT tháng",
        type="ktt",
        week_number=0,
        weight=4,
        due_date=today
    )
    HomeworkScore.objects.create(student=student, homework=ktt, score=random.uniform(15, 20))

    # Thưởng và tổng kết
    Bonus.objects.create(
        student=student,
        month=month_str,
        diligence_score=random.randint(8, 10),
        voucher_score=random.randint(8, 10)
    )

    final_score = round(random.uniform(14, 19), 2)
    MonthlyReport.objects.create(
        student=student,
        month=month_str,
        final_score=final_score,
        note="Học tốt" if final_score >= 17 else "Cần cải thiện"
    )
