from django.urls import path
from .views import site
from .views import api

app_name = 'recipes'

urlpatterns = [
    path('', site.RecipeListViewHome.as_view(), name='home'),
    path('recipes/search/', site.RecipeListViewSearch.as_view(), name='search'),  # type: ignore
    path('recipes/category/<int:category_id>/', site.RecipeListViewCategory.as_view(), name='category'),
    path('recipes/<int:pk>/', site.RecipeDetailViewBase.as_view(), name='recipe'),
    # API Test
    path('recipes/api/v1', site.RecipeListViewHomeApi.as_view(), name='recipe_api'),
    path('recipes/api/v1/<int:pk>', site.RecipeDetailAPI.as_view(), name='recipe_api_v1_detail'),
    # Teoria
    path('recipes/theory/', site.theory, name='theory'),
    # Tag
    path('recipes/tags/<slug:slug>', site.RecipeListViewTag.as_view(), name='tags'),
    path('recipes/api/v2/', api.recipe_api_list, name='recipe_api_v2')
]