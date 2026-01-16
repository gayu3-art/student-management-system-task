from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from students.views import StudentViewSet

# API Router
router = DefaultRouter()
router.register(r'students', StudentViewSet, basename='api-student')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),  # Built-in auth views
    path('api/', include(router.urls)),  # REST API endpoints
    path('api-auth/', include('rest_framework.urls')),  # Browsable API login
    path('', include('students.urls')),  # Web interface
]
