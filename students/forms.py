from django import forms
from .models import Student

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['name', 'email', 'phone', 'course', 'date_of_joining']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Full Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'name@example.com'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '10-digit number'}),
            'course': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Course Name'}),
            'date_of_joining': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }
