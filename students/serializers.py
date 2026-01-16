from rest_framework import serializers
from django.utils import timezone
from datetime import date
from .models import Student


class StudentSerializer(serializers.ModelSerializer):
    """
    Enhanced serializer for the Student model.
    Converts Student instances to/from JSON format for API responses.
    Includes custom validation and computed fields.
    """
    # Computed read-only fields
    days_since_joining = serializers.SerializerMethodField()
    
    class Meta:
        model = Student
        fields = [
            'id', 
            'name', 
            'email', 
            'phone', 
            'course', 
            'date_of_joining',
            'days_since_joining'
        ]
        read_only_fields = ['id', 'days_since_joining']
    
    def get_days_since_joining(self, obj):
        """Calculate days since the student joined"""
        if obj.date_of_joining:
            delta = date.today() - obj.date_of_joining
            return delta.days
        return None
    
    def validate_phone(self, value):
        """
        Custom validation for phone number.
        Ensures it's exactly 10 digits.
        """
        if not value.isdigit():
            raise serializers.ValidationError("Phone number must contain only digits.")
        if len(value) != 10:
            raise serializers.ValidationError("Phone number must be exactly 10 digits.")
        return value
    
    def validate_email(self, value):
        """
        Custom validation for email.
        Ensures uniqueness when creating or updating.
        """
        # Check if updating existing student
        if self.instance:
            # Exclude current instance from uniqueness check
            if Student.objects.exclude(pk=self.instance.pk).filter(email=value).exists():
                raise serializers.ValidationError("A student with this email already exists.")
        else:
            # Creating new student
            if Student.objects.filter(email=value).exists():
                raise serializers.ValidationError("A student with this email already exists.")
        return value
    
    def validate_date_of_joining(self, value):
        """
        Ensure date of joining is not in the future.
        """
        if value > date.today():
            raise serializers.ValidationError("Date of joining cannot be in the future.")
        return value


class StudentListSerializer(serializers.ModelSerializer):
    """
    Lightweight serializer for list views.
    Excludes computed fields for better performance.
    """
    class Meta:
        model = Student
        fields = ['id', 'name', 'email', 'course', 'date_of_joining']

