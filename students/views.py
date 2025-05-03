from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from .models import Student
from .face_utils import extract_face_vector
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from .forms import ClassForm
from .models import Class, Schedule, TuitionRecord, Attendance, Homework, HomeworkScore, MonthlySummary
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils import timezone
from datetime import datetime, timedelta
from datetime import date
import openpyxl
from openpyxl.styles import Font, Alignment
from django.http import HttpResponse
from django.utils.timezone import now
import calendar

class RegisterFaceAPIView(APIView):
    parser_classes = [MultiPartParser]

    def post(self, request):
        image = request.data.get('image')
        student_code = request.data.get('student_code')
        student = Student.objects.filter(student_code=student_code).first()

        if not student:
            return Response({'error': 'Student not found'}, status=404)
        
        vector = extract_face_vector(image.read())
        if not vector:
            return Response({'error': 'Face not detected'}, status=400)
        
        student.face_vector = vector
        student.save()
        return Response({'message': 'Face vector saved sucessfully'})

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if user.is_superuser:
                return redirect('admin_dashboard')
            elif user.is_staff:
                return redirect('teacher_dashboard')
        else:
            return render(request, "login.html", {"error": "Sai tài khoản hoặc mật khẩu"})

    return render(request, "login.html")

@login_required
def admin_dashboard(request):
    return render(request, "admin_dashboard.html")

@login_required
def teacher_dashboard(request):
    return render(request, "teacher_dashboard.html")

def logout_view(request):
    logout(request)
    return redirect('/login/')

@login_required
def class_list_view(request):
    classes = Class.objects.all()
    return render(request, 'class_list.html', {'classes': classes})

@login_required
def create_class_view(request):
    if request.method == 'POST':
        form = ClassForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('class_list')
    else:
        form = ClassForm()
    return render(request, 'class_form.html', {'form': form, 'action': 'Thêm'})

@login_required
def edit_class_view(request, class_id):
    cls = Class.objects.get(id=class_id)
    if request.method == 'POST':
        form = ClassForm(request.POST, instance=cls)
        if form.is_valid():
            form.save()
            return redirect('class_list')
    else:
        form = ClassForm(instance=cls)
    return render(request, 'class_form.html', {'form': form, 'action': 'Sửa'})

@login_required
def delete_class_view(request, class_id):
    cls = Class.objects.get(id=class_id)
    cls.delete()
    return redirect('class_list')

@login_required
def student_list_view(request):
    query = request.GET.get('q', '')
    class_id = request.GET.get('class_id')

    students = Student.objects.select_related('class_obj')

    if query:
        students = students.filter(
            Q(name__icontains=query) |
            Q(student_code__icontains=query) |
            Q(parent_phone__icontains=query)
        )

    if class_id:
        students = students.filter(class_obj__id=class_id)

    return render(request, 'student_list.html', {
        'students': students,
        'query': query,
        'class_id': int(class_id) if class_id else None,
        'classes': Class.objects.all(),
    })

@login_required
def create_student_view(request):
    classes = Class.objects.all()
    if request.method == "POST":
        Student.objects.create(
            student_code=request.POST.get('student_code'),
            name=request.POST.get('name'),
            class_obj_id=request.POST.get('class_obj'),
            parent_name=request.POST.get('parent_name'),
            parent_phone=request.POST.get('parent_phone'),
            student_phone=request.POST.get('student_phone'),
        )
        return redirect('student_list')
    return render(request, 'student_form.html', {'classes': classes})

@login_required
def update_student_view(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    classes = Class.objects.all()
    if request.method == "POST":
        student.student_code = request.POST.get('student_code')
        student.name = request.POST.get('name')
        student.class_obj_id = request.POST.get('class_obj')
        student.parent_name = request.POST.get('parent_name')
        student.parent_phone = request.POST.get('parent_phone')
        student.student_phone = request.POST.get('student_phone')
        student.save()
        return redirect('student_list')
    return render(request, 'student_form.html', {
        'student': student,
        'classes': classes
    })

@login_required
def delete_student_view(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    if request.method == "POST":
        student.delete()
        return redirect('student_list')
    return render(request, 'confirm_delete_student.html', {'student': student})

@login_required
def schedule_list(request):
    schedules = Schedule.objects.select_related('class_obj').all()
    return render(request, 'schedule_list.html', {'schedules': schedules})

@login_required
def schedule_create(request):
    classes = Class.objects.all()
    if request.method == 'POST':
        class_id = request.POST['class_id']
        day_of_week = request.POST['day_of_week']
        start_time = request.POST['start_time']
        end_time = request.POST['end_time']
        Schedule.objects.create(
            class_obj_id=class_id,
            day_of_week=day_of_week,
            start_time=start_time,
            end_time=end_time,
        )
        return redirect('schedule_list')
    return render(request, 'schedule_form.html', {'classes': classes})

@login_required
def schedule_edit(request, schedule_id):
    schedule = Schedule.objects.get(id=schedule_id)
    classes = Class.objects.all()
    if request.method == 'POST':
        schedule.class_obj_id = request.POST['class_id']
        schedule.day_of_week = request.POST['day_of_week']
        schedule.start_time = request.POST['start_time']
        schedule.end_time = request.POST['end_time']
        schedule.save()
        return redirect('schedule_list')
    return render(request, 'schedule_form.html', {'schedule': schedule, 'classes': classes})

@login_required
def schedule_delete(request, schedule_id):
    Schedule.objects.get(id=schedule_id).delete()
    return redirect('schedule_list')

@login_required
def tuition_list(request):
    # Lấy tháng hiện tại dạng "MM/YYYY"
    month = request.GET.get('month', timezone.now().strftime('%m/%Y'))
    class_id = request.GET.get('class_id')

    students = Student.objects.select_related('class_obj').all()
    if class_id:
        students = students.filter(class_obj__id=class_id)

    result = []
    for student in students:
        record = TuitionRecord.objects.filter(student=student, month=month).first()
        result.append({
            'student': student,
            'record': record,  # None nếu chưa gửi minh chứng
        })

    # Gợi ý danh sách tháng gần đây
    months = []
    now_date = timezone.now()
    for i in range(0, 6):
        past_month = (now_date.replace(day=1) - timezone.timedelta(days=30 * i))
        months.append(past_month.strftime('%m/%Y'))

    context = {
        'month': month,
        'class_id': int(class_id) if class_id else None,
        'students_records': result,
        'classes': Class.objects.all(),
        'months': months,
    }
    return render(request, 'tuition_list.html', context)

@login_required
def confirm_tuition_payment(request, record_id):
    record = get_object_or_404(TuitionRecord, pk=record_id)
    record.status = 'confirmed'
    record.approved_at = timezone.now()
    record.save()
    return redirect('tuition_list')



#xem tong hop cua lop theo thang
@login_required
def summary_view(request):
    selected_class_id = request.GET.get('class_id')
    selected_month = request.GET.get('month', datetime.now().strftime('%m/%Y'))

    classes = Class.objects.all()
    students = Student.objects.filter(class_obj__id=selected_class_id) if selected_class_id else []

    # Lấy danh sách buổi học trong tháng đó theo thứ tự
    month = datetime.strptime(selected_month, "%m/%Y")
    homework_list = Homework.objects.filter(
        class_obj__id=selected_class_id,
        type='btvn',
        date__month=month.month,
        date__year=month.year
    ).order_by('date')

    # Dùng để làm tiêu đề cột: Buổi 1 (02/04), Buổi 2 (06/04), ...
    column_headers = [f"Buổi {i+1} ({hw.date.strftime('%d/%m')})" for i, hw in enumerate(homework_list)]

    student_data = []
    for student in students:
        row = {
            'student': student,
            'scores': [],
            'attendances': [],
        }

        for hw in homework_list:
            score = HomeworkScore.objects.filter(homework=hw, student=student).first()
            row['scores'].append(score.score if score else '')

            attendance = Attendance.objects.filter(student=student, date=hw.date).first()
            if attendance:
                if attendance.status == 'on_time':
                    row['attendances'].append("✅")
                elif attendance.status == 'late':
                    row['attendances'].append("🕒")
                else:
                    row['attendances'].append("❌")
            else:
                row['attendances'].append("-")

        # Tổng kết nếu có
        summary = MonthlySummary.objects.filter(student=student, month=selected_month).first()
        row['summary'] = summary

        student_data.append(row)

    context = {
        'classes': classes,
        'selected_class_id': int(selected_class_id) if selected_class_id else None,
        'selected_month': selected_month,
        'column_headers': column_headers,
        'homework_list': homework_list,
        'student_data': student_data,
    }
    return render(request, 'summary_view.html', context)

#nhap diem btvn cho hsinh
@login_required
def homework_score_entry(request):
    classes = Class.objects.all()
    selected_class_id = request.GET.get('class_id')
    selected_date = request.GET.get('date') or date.today().isoformat()

    students = []
    scores = {}

    if request.method == 'POST':
        class_id = request.POST.get('class_id')
        date_str = request.POST.get('date')
        homework, _ = Homework.objects.get_or_create(
            class_obj_id=class_id,
            date=date_str,
            defaults={'type': 'btvn'}
        )

        for key in request.POST:
            if key.startswith('score_'):
                student_id = key.split('_')[1]
                score = request.POST[key]
                student = Student.objects.get(id=student_id)
                if score:
                    HomeworkScore.objects.update_or_create(
                        student=student,
                        homework=homework,
                        defaults={'score': float(score)}
                    )
        return redirect(f"{request.path}?class_id={class_id}&date={date_str}")

    elif selected_class_id:
        students = Student.objects.filter(class_obj_id=selected_class_id)
        homework = Homework.objects.filter(class_obj_id=selected_class_id, date=selected_date).first()
        if homework:
            for student in students:
                score_obj = HomeworkScore.objects.filter(student=student, homework=homework).first()
                scores[student.id] = score_obj.score if score_obj else ''

    return render(request, 'homework_score_entry.html', {
        'classes': classes,
        'students': students,
        'selected_class_id': selected_class_id,
        'selected_date': selected_date,
        'scores': scores
    })

# nhap link bai tap cho buoi hoc
@login_required
def homework_link_entry(request):
    classes = Class.objects.all()
    selected_class_id = request.GET.get('class_id')
    selected_date = request.GET.get('date') or date.today().isoformat()
    existing_link = ""

    if request.method == 'POST':
        class_id = request.POST.get('class_id')
        date_str = request.POST.get('date')
        link = request.POST.get('link')

        homework, created = Homework.objects.get_or_create(
            class_obj_id=class_id,
            date=date_str,
            defaults={'type': 'btvn', 'link': link}
        )
        if not created:
            homework.link = link
            homework.save()
        return redirect(f"{request.path}?class_id={class_id}&date={date_str}")

    if selected_class_id:
        hw = Homework.objects.filter(class_obj_id=selected_class_id, date=selected_date).first()
        if hw:
            existing_link = hw.link

    return render(request, 'homework_link_entry.html', {
        'classes': classes,
        'selected_class_id': selected_class_id,
        'selected_date': selected_date,
        'existing_link': existing_link,
    })

def calculate_diligence_score(attendance_list):
    total_sessions = len(attendance_list)
    if total_sessions == 0:
        return 0

    score = 0
    for status in attendance_list:
        if status == 'on_time':
            score += 1
        elif status == 'late':
            score += 0.75
        # absent = 0 điểm

    return round((score / total_sessions) * 10, 2)

def calculate_btvn_avg(student, start_date, end_date):
    # Lấy danh sách bài tập về nhà của lớp trong tháng
    homeworks = Homework.objects.filter(
        class_obj=student.class_obj,
        date__range=(start_date, end_date),
        type='btvn'
    )
    # Lấy điểm BTVN của học sinh
    scores = HomeworkScore.objects.filter(
        student=student,
        homework__in=homeworks
    ).values_list('score', flat=True)

    if scores:
        return round(sum(scores) / len(scores), 2)
    return 0
#nhap diem ktt

@login_required
def monthly_summary_entry(request):
    classes = Class.objects.all()
    month = request.GET.get("month", now().strftime("%m/%Y"))
    class_id = request.GET.get("class_id")

    students = Student.objects.filter(class_obj__id=class_id) if class_id else []

    # Tách tháng/năm để tính khoảng thời gian
    try:
        m, y = map(int, month.split("/"))
    except:
        m, y = now().month, now().year

    start_date = datetime(y, m, 1).date()
    end_date = datetime(y, m, calendar.monthrange(y, m)[1]).date()

    if request.method == "POST":
        for student in students:
            ktt_score = request.POST.get(f'ktt_{student.id}')
            voucher_score = request.POST.get(f'voucher_{student.id}')
            diligence_score = request.POST.get(f'diligence_{student.id}')
            final = None
            try:
                btvn_avg = calculate_btvn_avg(student, start_date, end_date)
                ktt = float(ktt_score or 0)
                voucher = float(voucher_score or 0)
                diligence = float(diligence_score or 0)
                final = round((btvn_avg + ktt * 4 + voucher + diligence) / 7, 2)
            except:
                pass

            MonthlySummary.objects.update_or_create(
                student=student, month=month,
                defaults={
                    'ktt_score': ktt_score or None,
                    'voucher_score': voucher_score or None,
                    'diligence_score': diligence_score or None,
                    'final_score': final
                }
            )
        return redirect('monthly_summary_entry')

    # GET: gợi ý điểm chuyên cần
    summary_data = []
    for student in students:
        attendances = Attendance.objects.filter(
            student=student,
            date__range=(start_date, end_date)
        ).values_list('status', flat=True)
        diligence_score = calculate_diligence_score(attendances)

        summary, _ = MonthlySummary.objects.get_or_create(student=student, month=month)
        summary_data.append({
            'student': student,
            'summary': summary,
            'suggested_diligence': diligence_score
        })

    return render(request, 'monthly_summary_entry.html', {
        'classes': classes,
        'class_id': int(class_id) if class_id else None,
        'month': month,
        'summary_data': summary_data,
    })

from io import BytesIO
import pandas as pd
@login_required
def export_excel(request):
    class_id = request.GET.get("class_id")
    month = request.GET.get("month")  # format: YYYY-MM

    if not class_id or not month:
        classes = Class.objects.all()
        return render(request, "export_excel_form.html", {
            "classes": classes,
            "default_month": now().strftime("%Y-%m")
        })

    try:
        y, m = map(int, month.split("-"))
        month_str = f"{m:02d}/{y}"
    except:
        return HttpResponse("Tháng không hợp lệ", status=400)

    start_date = datetime(y, m, 1).date()
    end_date = datetime(y, m, calendar.monthrange(y, m)[1]).date()
    
    class_obj = Class.objects.get(id=class_id)
    students = Student.objects.filter(class_obj=class_obj).order_by("name")

    rows = []
    for i, student in enumerate(students, start=1):
        summary = MonthlySummary.objects.filter(student=student, month=month_str).first()

        homeworks = Homework.objects.filter(class_obj=class_obj, type='btvn', date__range=(start_date, end_date))
        scores = HomeworkScore.objects.filter(student=student, homework__in=homeworks).values_list('score', flat=True)
        btvn_avg = round(sum(scores) / len(scores), 2) if scores else 0

        rows.append({
            "STT": i,
            "Họ tên": student.name,
            "Lớp": class_obj.name,
            "BTVN TB": btvn_avg,
            "Chuyên cần": summary.diligence_score if summary else '',
            "Voucher": summary.voucher_score if summary else '',
            "KTT": summary.ktt_score if summary else '',
            "Tổng kết": summary.final_score if summary else '',
        })

    df = pd.DataFrame(rows)
    output = BytesIO()
    df.to_excel(output, index=False, sheet_name="Tổng kết tháng")
    output.seek(0)

    filename = f"tong_ket_{class_obj.name}_{month_str}.xlsx"
    response = HttpResponse(output, content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    response["Content-Disposition"] = f"attachment; filename={filename}"
    return response

#nhap tinh trang diem danh
@login_required
def attendance_entry(request):
    classes = Class.objects.all()
    selected_class_id = request.GET.get('class_id')
    selected_date = request.GET.get('date')

    students = Student.objects.filter(class_obj__id=selected_class_id) if selected_class_id else []

    # Nếu có ngày thì convert thành date object
    date_obj = None
    if selected_date:
        try:
            date_obj = datetime.strptime(selected_date, "%Y-%m-%d").date()
        except:
            pass

    # POST để cập nhật tình trạng
    if request.method == "POST" and date_obj:
        for student in students:
            status = request.POST.get(f'status_{student.id}')
            if status:
                Attendance.objects.update_or_create(
                    student=student, date=date_obj,
                    defaults={'status': status}
                )
        return redirect(f'{request.path}?class_id={selected_class_id}&date={selected_date}')

    attendance_data = []
    for student in students:
        status_icon = "-"
        if date_obj:
            att = Attendance.objects.filter(student=student, date=date_obj).first()
            if att:
                if att.status == "on_time":
                    status_icon = "✅"
                elif att.status == "late":
                    status_icon = "🕒"
                elif att.status == "absent":
                    status_icon = "❌"
        attendance_data.append({'student': student, 'status_icon': status_icon})

    return render(request, 'attendance_entry.html', {
        'classes': classes,
        'selected_class_id': int(selected_class_id) if selected_class_id else None,
        'selected_date': selected_date,
        'attendance_data': attendance_data,
    })
