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
    path('logout/', views.logout_view, name='logout'),
    # Dashboard
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/recipe/new/', views.dashboard_recipe_create, name='dashboard_recipe_new'),
    path('dashboard/recipe/<int:id>/edit/', views.dashboard_recipe_edit, name='dashboard_recipe_edit'),
    path('dashboard/recipe/<int:id>/delete/', views.dashboard_recipe_delete, name='dashboard_recipe_delete'),
]   