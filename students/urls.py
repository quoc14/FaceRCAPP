from django.urls import path
from .views import RegisterFaceAPIView
from . import views
from .views import (
    RegisterFaceAPIView, login_view, logout_view,
    admin_dashboard, teacher_dashboard,
    class_list_view, create_class_view, edit_class_view, delete_class_view
)
urlpatterns = [
    path('api/register-face/', RegisterFaceAPIView.as_view()),
    path('login/', views.login_view, name='login'),
    path('dashboard/admin/', views.admin_dashboard, name='admin_dashboard'),
    path('dashboard/teacher/', views.teacher_dashboard, name='teacher_dashboard'),
    path('logout/', views.logout_view, name='logout'),

    # 💡 Thêm các route lớp học
    path('center-admin/classes/', class_list_view, name='class_list'),
    path('center-admin/classes/create/', create_class_view, name='create_class'),
    path('center-admin/classes/<int:class_id>/edit/', edit_class_view, name='edit_class'),
    path('center-admin/classes/<int:class_id>/delete/', delete_class_view, name='delete_class'),

    # route hoc sinh
    path('center-admin/students/', views.student_list_view, name='student_list'),
    path('center-admin/students/create/', views.create_student_view, name='create_student'),
    path('center-admin/students/<int:student_id>/update/', views.update_student_view, name='update_student'),
    path('center-admin/students/<int:student_id>/delete/', views.delete_student_view, name='delete_student'),
    # Lịch học
    path('center-admin/schedules/', views.schedule_list, name='schedule_list'),
    path('center-admin/schedules/create/', views.schedule_create, name='schedule_create'),
    path('center-admin/schedules/<int:schedule_id>/edit/', views.schedule_edit, name='schedule_edit'),
    path('center-admin/schedules/<int:schedule_id>/delete/', views.schedule_delete, name='schedule_delete'),
    path('center-admin/tuition/', views.tuition_list, name='tuition_list'),
    path('center-admin/tuition/confirm/<int:record_id>/', views.confirm_tuition_payment, name='confirm_tuition'),

    # tong ket lop theo thang cua hoc sinh
    path('teacher/summary/', views.summary_view, name='summary_view'),
    #nhapdiem
    path('teacher/homework-score/', views.homework_score_entry, name='homework_score_entry'),
    #nhap link bai tap
    path('teacher/homework-link/', views.homework_link_entry, name='homework_link_entry'),
    ## nhap diem voucher, ktt
    path('teacher/monthly-summary/', views.monthly_summary_entry, name='monthly_summary_entry'),
    #xuat file tong ket thang
    path('teacher/export-summary/', views.export_excel, name='export_excel'),
    #nhap tinh trang diem danh
    path('teacher/attendance-entry/', views.attendance_entry, name='attendance_entry'),



]
