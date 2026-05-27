from django.db import models
from django.contrib.auth.models import User


class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    roll_number = models.CharField(max_length=20, unique=True) # Added unique=True
    course = models.CharField(max_length=100)

    def __str__(self):
        return self.user.username


class Subject(models.Model):
    name = models.CharField(max_length=100)
    # Changed from CharField to ForeignKey
    teacher = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True, related_name='subjects')
    syllabus = models.TextField()

    def __str__(self):
        return self.name


class Attendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='attendance_records')
    # Pointed to Teacher model instead of User model
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE) 
    status = models.BooleanField(default=False)
    date = models.DateField(auto_now_add=True)

    class Meta:
        # Prevents duplicate attendance entries for the same student on the same day
        unique_together = ['student', 'date']

    def __str__(self):
        return f"{self.student.user.username} - {self.date}"


class Marks(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='marks')
    # Changed from CharField to ForeignKey
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE) 
    marks = models.IntegerField()

    def __str__(self):
        return f"{self.student.user.username} - {self.subject.name}"