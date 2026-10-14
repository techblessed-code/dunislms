from django.urls import path
from .views import  CourseCRUDAPIView, CourseListCreateAPIView, CourseDetailAPIView


urlpatterns = [
    path('', CourseCRUDAPIView.as_view(), name='course_crud_api'),
    
    # Compatibility named used by older templates/tests
    path('', CourseListCreateAPIView.as_view(), name='course_api'),
    path('<int:pk>/', CourseDetailAPIView.as_view(), name='course_detail'),
]