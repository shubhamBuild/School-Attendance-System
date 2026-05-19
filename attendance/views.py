from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import Attendance, Teacher, Student
from .forms import AttendanceForm


def dashboard(request):
    total_students = Student.objects.count()
    total_attendance = Attendance.objects.count()

    context = {
        'students': total_students,
        'attendance': total_attendance,
    }

    return render(request, 'dashboard.html', context)

@login_required
#def mark_attendance(request):
def mark_attendance(request):
    if request.method == 'POST':
        form = AttendanceForm(request.POST)

        if form.is_valid():
            attendance = form.save(commit=False)
            attendance.teacher = request.user
            attendance.save()

            return redirect('dashboard')

    else:
        form = AttendanceForm()

    return render(request, 'mark_attendance.html', {'form': form})


def attendance_list(request):
    records = Attendance.objects.all().order_by('-date')
    return render(request, 'attendance_list.html', {'records': records})