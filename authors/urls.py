# Django
from django.urls import include, path

# Views
from . import views
from authors.views import api

# Rest Framework
from rest_framework.routers import SimpleRouter

app_name = 'authors'

author_api_router = SimpleRouter()
author_api_router.register('', api.AuthorViewSet, basename='author-api')


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
    path('dashboard/recipe/new/', views.DashboardRecipeCreate.as_view(), name='dashboard_recipe_new'),
    path('dashboard/recipe/delete/', views.DashboardRecipeDelete.as_view(), name='dashboard_recipe_delete'),
    path('dashboard/recipe/<int:id>/edit/', views.DashboardRecipeEdit.as_view(), name='dashboard_recipe_edit'),
    # Profile
    path('profile/<int:id>', views.ProfileView.as_view(), name='profile'),

    # API - View Set
    path('api/', include(author_api_router.urls)),
]   