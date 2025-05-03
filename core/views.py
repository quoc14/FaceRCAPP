from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if user.is_superuser:
                return redirect("admin_dashboard")
            elif user.is_staff:
                return redirect("teacher_dashboard")
            else:
                return render(request, "login.html", {"error": "Bạn không có quyền truy cập"})
        else:
            return render(request, "login.html", {"error": "Sai tên đăng nhập hoặc mật khẩu"})
    return render(request, "login.html")

@login_required
def admin_dashboard(request):
    return render(request, "admin_dashboard.html")

@login_required
def teacher_dashboard(request):
    return render(request, "teacher_dashboard.html")
