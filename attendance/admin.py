from django.contrib import admin
from .models import Student, Teacher, Attendance, Subject, Marks

admin.site.register(Student)
admin.site.register(Teacher)
admin.site.register(Attendance)
admin.site.register(Subject)
admin.site.register(Marks)