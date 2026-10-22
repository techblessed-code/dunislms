from django.urls import path
from .views import CourseCreateAPIView, CourseDetailAPIView


# NOTE: this file previously imported CourseListCreateAPIView (which never
# existed - ImportError at startup) and defined TWO routes for the same path '',
# the second of which could never be reached. It is now one list/create route
# plus one detail route.
urlpatterns = [
    # List all courses (GET) and create a course (POST)
    path('', CourseCreateAPIView.as_view(), name='course_crud_api'),

    # Retrieve (GET), update (PUT/PATCH) and delete (DELETE) a single course
    path('<int:pk>/', CourseDetailAPIView.as_view(), name='course_detail_api'),
]
