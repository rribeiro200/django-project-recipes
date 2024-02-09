from django.urls import path
from . import views

app_name = 'recipes'

urlpatterns = [
    path('', views.RecipeListViewHome.as_view(), name='home'),
    path('recipes/search/', views.RecipeListViewSearch.as_view(), name='search'),  # type: ignore
    path('recipes/category/<int:category_id>/', views.RecipeListViewCategory.as_view(), name='category'),
    path('recipes/<int:pk>/', views.RecipeDetailViewBase.as_view(), name='recipe'),
    # API
    path('recipes/api/v1', views.RecipeListViewHomeApi.as_view(), name='recipe_api'),
    path('recipes/api/v1/<int:pk>', views.RecipeDetailAPI.as_view(), name='recipe_api_v1_detail'),
    # Teoria
    path('recipes/theory/', views.theory, name='theory'),
]