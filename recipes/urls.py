# Django
from django.urls import include, path

# Views
from .views import site
from .views import api

# Rest Framework
from rest_framework.routers import SimpleRouter

app_name = 'recipes'

recipe_api_v2_router = SimpleRouter()
recipe_api_v2_router.register('', api.RecipeAPIv2ViewSet, basename='recipes-api')

urlpatterns = [
    path('', site.RecipeListViewHome.as_view(), name='home'),
    path('recipes/search/', site.RecipeListViewSearch.as_view(), name='search'),  # type: ignore
    path('recipes/category/<int:category_id>/', site.RecipeListViewCategory.as_view(), name='category'),
    path('recipes/<int:pk>/', site.RecipeDetailViewBase.as_view(), name='recipe'),
    
    # API - V1
    path('recipes/api/v1', site.RecipeListViewHomeApi.as_view(), name='recipe_api'),
    path('recipes/api/v1/<int:pk>', site.RecipeDetailAPI.as_view(), name='recipe_api_v1_detail'),
    
    # Teoria
    path('recipes/theory/', site.theory, name='theory'),
    
    # Tag
    path('recipes/tags/<slug:slug>', site.RecipeListViewTag.as_view(), name='tags'),
    
    # API - V2
    path('recipes/api/v2/', include(recipe_api_v2_router.urls)),
    path('recipes/api/v2/tag/<int:pk>/', api.TagAPIV2Detail.as_view(), name='recipe_api_v2_tag'),
]