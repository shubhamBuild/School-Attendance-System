from django import forms
from .models import Attendance, Student

class AttendanceForm(forms.ModelForm):

    student = forms.ModelChoiceField(
        queryset=Student.objects.all(),
        empty_label="Select Student Name"
    )

    class Meta:
        model = Attendance
        fields = ['student', 'status']

        widgets = {
            'student': forms.Select(attrs={
                'class': 'form-select'
            }),

            'status': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }