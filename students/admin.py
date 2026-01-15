from django.contrib import admin
from .models import Student

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'course', 'date_of_joining')
    search_fields = ('name', 'email', 'phone')
    list_filter = ('course', 'date_of_joining')
