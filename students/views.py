from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin # Optional but nice
from django.db.models import Q
from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Student
from .forms import StudentForm
from .serializers import StudentSerializer, StudentListSerializer

class StudentListView(LoginRequiredMixin, ListView):
    model = Student
    template_name = 'students/student_list.html'
    context_object_name = 'students'
    ordering = ['-date_of_joining']
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(name__icontains=query) |
                Q(email__icontains=query) |
                Q(course__icontains=query)
            )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q', '')
        return context

class StudentDetailView(LoginRequiredMixin, DetailView):
    model = Student
    template_name = 'students/student_detail.html'
    context_object_name = 'student'

class StudentCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Student
    form_class = StudentForm
    template_name = 'students/student_form.html'
    success_message = "Student created successfully!"

class StudentUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Student
    form_class = StudentForm
    template_name = 'students/student_form.html'
    success_message = "Student updated successfully!"

class StudentDeleteView(LoginRequiredMixin, DeleteView):
    model = Student
    template_name = 'students/student_confirm_delete.html'
    success_url = reverse_lazy('student-list')
    context_object_name = 'student'


# REST API ViewSet
class StudentViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows students to be viewed, created, edited or deleted.
    
    Provides:
    - GET /api/students/ - List all students (paginated, searchable, filterable)
    - POST /api/students/ - Create a new student
    - GET /api/students/{id}/ - Retrieve a specific student
    - PUT/PATCH /api/students/{id}/ - Update a student
    - DELETE /api/students/{id}/ - Delete a student
    - GET /api/students/statistics/ - Get student statistics
    - POST /api/students/bulk_create/ - Create multiple students at once
    
    Filtering:
    - ?course=Computer Science - Filter by course
    - ?search=John - Search in name, email, course
    - ?ordering=-date_of_joining - Order by field (prefix with - for descending)
    """
    queryset = Student.objects.all().order_by('-date_of_joining')
    serializer_class = StudentSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'email', 'course']
    ordering_fields = ['name', 'date_of_joining', 'course', 'email']
    filterset_fields = ['course']
    
    def get_serializer_class(self):
        """
        Use lightweight serializer for list view for better performance.
        """
        if self.action == 'list':
            return StudentListSerializer
        return StudentSerializer
    
    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """
        Custom endpoint to get student statistics.
        GET /api/students/statistics/
        """
        from django.db.models import Count
        from datetime import date, timedelta
        
        total_students = Student.objects.count()
        
        # Students by course
        by_course = Student.objects.values('course').annotate(
            count=Count('id')
        ).order_by('-count')
        
        # Recent students (joined in last 30 days)
        thirty_days_ago = date.today() - timedelta(days=30)
        recent_students = Student.objects.filter(
            date_of_joining__gte=thirty_days_ago
        ).count()
        
        return Response({
            'total_students': total_students,
            'students_by_course': list(by_course),
            'recent_students_30_days': recent_students,
        })
    
    @action(detail=False, methods=['post'])
    def bulk_create(self, request):
        """
        Create multiple students at once.
        POST /api/students/bulk_create/
        
        Body: {
            "students": [
                {"name": "...", "email": "...", ...},
                {"name": "...", "email": "...", ...}
            ]
        }
        """
        students_data = request.data.get('students', [])
        
        if not isinstance(students_data, list):
            return Response(
                {'error': 'Expected a list of students'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        serializer = self.get_serializer(data=students_data, many=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        return Response(
            {
                'message': f'{len(students_data)} students created successfully',
                'students': serializer.data
            },
            status=status.HTTP_201_CREATED
        )

