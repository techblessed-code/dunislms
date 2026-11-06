from django.urls import path
from django.contrib.auth import views as auth_Views
from .import views

# Namespace so URLs are reversed as 'users:...' everywhere
# (templates already use the users:... prefix).
app_name = 'users'

urlpatterns = [
    path('login/', auth_Views.LoginView.as_view(template_name='users/login.html'), name='login'),
    # Self-service sign-up (new — accounts are no longer admin-only)
    path('register/', views.register, name='register'),
    path('logout/', auth_Views.LogoutView.as_view(), name='logout'),
    path('dashboard/', views.dashboard,name='dashboard')
]
