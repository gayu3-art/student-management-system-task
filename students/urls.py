from django.urls import path
from .views import (
    StudentListView,
    StudentDetailView,
    StudentCreateView,
    StudentUpdateView,
    StudentDeleteView
)

urlpatterns = [
    path('', StudentListView.as_view(), name='student-list'),
    path('student/<int:pk>/', StudentDetailView.as_view(), name='student-detail'),
    path('student/new/', StudentCreateView.as_view(), name='student-create'),
    path('student/<int:pk>/edit/', StudentUpdateView.as_view(), name='student-update'),
    path('student/<int:pk>/delete/', StudentDeleteView.as_view(), name='student-delete'),
]
