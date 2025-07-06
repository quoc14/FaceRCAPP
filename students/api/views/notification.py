from rest_framework.decorators import api_view
from rest_framework.response import Response
from students.models import Student, Notification

@api_view(['GET'])
def student_notifications(request, student_code):
    student = Student.objects.filter(student_code=student_code).first()
    if not student:
        return Response({'error': 'Không tìm thấy học sinh'}, status=404)

    notifications = Notification.objects.filter(
        target_class__isnull=True
    ) | Notification.objects.filter(target_class=student.class_obj)

    notifications = notifications.order_by('-created_at')[:30]

    return Response([
        {
            "title": n.title,
            "message": n.message,
            "created_at": n.created_at.strftime("%d/%m/%Y %H:%M"),
        }
        for n in notifications
    ])
