from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from .models import Attendance, Teacher, Student, Marks, Subject # Added missing imports
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
def mark_attendance(request):
    # Ensure the user is actually a teacher before proceeding
    try:
        teacher_profile = request.user.teacher
    except ObjectDoesNotExist:
        # Redirect non-teachers away from this page (e.g., back to dashboard)
        return redirect('dashboard') 

    if request.method == 'POST':
        form = AttendanceForm(request.POST)
        if form.is_valid():
            attendance = form.save(commit=False)
            attendance.teacher = teacher_profile # Assign the Teacher instance, not User
            attendance.save()
            return redirect('dashboard')
    else:
        form = AttendanceForm()

    return render(request, 'mark_attendance.html', {'form': form})


def attendance_list(request):
    # select_related fetches the connected student and teacher data in one go
    # This prevents the N+1 query performance issue in your templates
    records = Attendance.objects.select_related('student__user', 'teacher__user').order_by('-date')
    
    return render(request, 'attendance_list.html', {'records': records})


@login_required
def student_dashboard(request):
    # Safely fetch the student profile, or return a 404 page if a teacher tries to view this
    student = get_object_or_404(Student, user=request.user)

    # Use select_related to optimize these queries as well
    attendance = Attendance.objects.filter(student=student).select_related('teacher__user')
    marks = Marks.objects.filter(student=student).select_related('subject')
    subjects = Subject.objects.select_related('teacher__user').all()

    context = {
        'student': student,
        'attendance': attendance,
        'marks': marks,
        'subjects': subjects,
    }

    return render(request, 'student_dashboard.html', context)