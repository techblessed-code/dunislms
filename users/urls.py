from django.urls import path
from django.contrib.auth import views as auth_Views
from .import views

urlpatterns = [
    path('login/', auth_Views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_Views.LogoutView.as_view(), name='logout'),
    path('dashboard/', views.dashboard,name='dashboard')
]
