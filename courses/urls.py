from django.urls import path
from . import  views

urlpatterns = [
    path('', views.course_list, name='course_list'),
    path('about/', views.about, name='about'),
    path('course-table/', views.course_table, name='course_table'),
    path('create-course/', views.create_course, name='create_course'),
    path('<int:course_id>/', views.course_details, name='course_details'),
    path('admin/', views.course_list, name='admin_course_list')

 ]

