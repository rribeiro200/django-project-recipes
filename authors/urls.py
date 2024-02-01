from django.urls import path
from . import views

app_name = 'authors'

urlpatterns = [
    # Register
    path('register/', views.register_view, name='register'),
    path('register/create/', views.register_create, name='register_create'),
    # Login
    path('login/', views.login_view, name='login'),
    path('login/create', views.login_create, name='login_create'),
    # Logout
    path('logout/', views.logout_view, name='logout')
]   