from django.urls import path
from students.api.views.auth import student_login
from students.api.views.profile import student_profile
from students.api.views.face import register_face
from .views.schedule import schedule_today
from students.api.views.attendance import face_checkin_api
from students.api.views.homework import homework_summary_view
from students.api.views.monthly import monthly_summary_view
from students.api.views.tuition import get_tuition_info
from students.api.views.tuition import confirm_tuition_payment
from students.api.views.changepassword import change_password
urlpatterns = [
    #login
    path('auth/login/', student_login, name='student_login'),
    # lay thong tin hoc sinh
    path('student-profile/<str:student_code>/', student_profile, name='student_profile'),
    #dang ky khuon mat
    path('face/register/', register_face, name='register_face'),
    #lay lich hoc hom nay
    path('classes/schedule-today/<str:student_code>/', schedule_today, name='schedule_today'),
    # diem danh bang khuon mat
    path('attendance/face-checkin/', face_checkin_api),
    #xem diem va link btvn
    path("homework-summary/<str:student_code>/", homework_summary_view, name="homework_summary"),

    # xem tong ket thang
    
    path("monthly-summary/<int:student_id>/", monthly_summary_view, name="monthly_summary_api"),
    #xem thong tin hoc phi
    path('tuition/<int:student_id>/', get_tuition_info, name='get_tuition_info'),
    #gui minh chung
    path('tuition/confirm-payment/', confirm_tuition_payment, name='confirm_tuition_payment'),
    # change-password
    path('auth/change-password/', change_password, name='change_password'),



]
