import uuid
from django.db import models

class Class(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=10)
    grade = models.IntegerField()
    level = models.CharField(max_length=10)
    room = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return self.name

class Student(models.Model):
    id = models.BigAutoField(primary_key=True)
    student_code = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=100)
    class_obj = models.ForeignKey(Class, on_delete=models.CASCADE, related_name='students')
    parent_name = models.CharField(max_length=100, blank=True)
    parent_phone = models.CharField(max_length=20, blank=True)
    student_phone = models.CharField(max_length=20, blank=True)
    face_vector = models.JSONField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

class Teacher(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)

class TeachingAssignment(models.Model):
    id = models.BigAutoField(primary_key=True)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    class_obj = models.ForeignKey(Class, on_delete=models.CASCADE)

class Schedule(models.Model):
    id = models.BigAutoField(primary_key=True)
    class_obj = models.ForeignKey(Class, on_delete=models.CASCADE, related_name='schedules')
    day_of_week = models.IntegerField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    slot_name = models.CharField(max_length=50, blank=True)  # slot_name không cần nhập

    def save(self, *args, **kwargs):
        # Tự động gán slot_name theo thứ
        day_map = {
            2: "T2", 3: "T3", 4: "T4", 5: "T5",
            6: "T6", 7: "T7", 8: "CN"
        }
        self.slot_name = day_map.get(self.day_of_week, f"T{self.day_of_week}")
        super().save(*args, **kwargs)

class Attendance(models.Model):
    id = models.BigAutoField(primary_key=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    date = models.DateField()
    status = models.CharField(max_length=10, choices=[
        ('on_time', 'Đúng giờ'),
        ('late', 'Đi muộn'),
        ('absent', 'Vắng')
    ])

class Homework(models.Model):
    id = models.BigAutoField(primary_key=True)
    class_obj = models.ForeignKey(Class, on_delete=models.CASCADE)
    date = models.DateField()
    week_number = models.IntegerField(null=True, blank=True)
    type = models.CharField(max_length=10, choices=[('btvn', 'BTVN'), ('ktt', 'Kiểm tra')])
    link = models.URLField(blank=True)

class HomeworkScore(models.Model):
    id = models.BigAutoField(primary_key=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    homework = models.ForeignKey(Homework, on_delete=models.CASCADE)
    score = models.FloatField()

class MonthlySummary(models.Model):
    id = models.BigAutoField(primary_key=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    month = models.CharField(max_length=10)
    final_score = models.FloatField(null=True, blank=True)
    ktt_score = models.FloatField(null=True, blank=True)
    voucher_score = models.FloatField(null=True, blank=True)
    diligence_score = models.FloatField(null=True, blank=True)

    class Meta:
        unique_together = ('student', 'month')

class TuitionRecord(models.Model):
    id = models.BigAutoField(primary_key=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    month = models.CharField(max_length=10)
    amount = models.IntegerField(default=1000000)
    proof_image = models.ImageField(upload_to='tuition_proofs/', blank=True, null=True)
    submitted_at = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=10, choices=[
        ('pending', 'Chờ duyệt'),
        ('confirmed', 'Đã duyệt')
    ], default='pending')
    approved_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ('student', 'month')
