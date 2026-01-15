from django.db import models
from django.core.validators import RegexValidator
from django.urls import reverse

class Student(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True, error_messages={'unique': "A student with this email already exists."})
    
    phone_regex = RegexValidator(
        regex=r'^\d{10}$',
        message="Phone number must be exactly 10 digits."
    )
    phone = models.CharField(validators=[phone_regex], max_length=10)
    
    course = models.CharField(max_length=100)
    date_of_joining = models.DateField()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('student-detail', kwargs={'pk': self.pk})
