# Models Manipulation
from django.db.models.aggregates import Count
from django.db.models.query import QuerySet
from recipes.models import Recipe, Category
from django.db.models import Q, F, Value
from django.forms.models import model_to_dict
from django.db.models.functions import Concat
from tag.models import Tag

from typing import Any
from django.http.response import HttpResponse as HttpResponse
from django.shortcuts import render, get_list_or_404, get_object_or_404
from utils.pagination import make_pagination
from utils.recipes.factory import make_recipe
from django.http import Http404, HttpRequest, HttpResponse, HttpResponse as HttpResponse, JsonResponse
from django.core.paginator import Paginator
import os
from django.views.generic import ListView, DetailView

PER_PAGE = int(os.environ.get('PER_PAGE', 9))

class RecipeListViewBase(ListView):
    model = Recipe
    context_object_name = 'recipes'
    ordering = ['-id']
    template_name = 'recipes/pages/home.html'

    def get_queryset(self, *args, **kwargs) -> QuerySet[Recipe]:
        qs = super().get_queryset(*args, **kwargs)
        qs = qs.filter(
            is_published=True,
        )
        qs = qs.prefetch_related('author', 'category')
        qs = qs.prefetch_related('tags', 'author__profile')
        
        return qs
    
    def get_context_data(self, *args, **kwargs: Any) -> dict[str, Any]:
        ctx = super().get_context_data(*args, **kwargs)
        page_obj, pagination_range = make_pagination(self.request, ctx.get('recipes'),PER_PAGE)
        ctx.update({
            'recipes': page_obj,
            'pagination_range': pagination_range
        })

        return ctx


class RecipeListViewHome(RecipeListViewBase):
    template_name = 'recipes/pages/home.html'

# ListView API
class RecipeListViewHomeApi(RecipeListViewBase):
    template_name = 'recipes/pages/home.html'

    def render_to_response(self, context: dict[str, Any], **response_kwargs: Any) -> HttpResponse:
        recipe = self.get_context_data()['recipes']
        recipe_list = list(recipe.object_list.values())

        return JsonResponse(
            recipe_list,
            safe=False
        )    


class RecipeListViewCategory(RecipeListViewBase):
    template_name = 'recipes/pages/category.html'

    def get_queryset(self, *args, **kwargs) -> QuerySet[Recipe]:
        qs = super().get_queryset(*args, **kwargs)
        qs = qs.filter(
            category__id=self.kwargs['category_id'],
            is_published=True
        )

        if not qs:
            raise Http404()

        return qs
    
    def get_context_data(self, *args, **kwargs: Any) -> dict[str, Any]:
        ctx = super().get_context_data(*args, **kwargs)
        object_list = ctx['object_list']
        category_name = object_list[0].category.name
        
        ctx.update({
            'title': f'{category_name} - Category |'
        })
        return ctx


class RecipeListViewSearch(RecipeListViewBase):
    template_name = 'recipes/pages/search.html'

    def get_search_term(self):
        search_term = self.request.GET.get('q', '')
        return str(search_term)

    def get_queryset(self, *args, **kwargs) -> QuerySet[Recipe]:
        qs = super().get_queryset(*args, **kwargs)
        search_term = self.get_search_term()
        
        if not search_term:
            raise Http404()

        qs = qs.filter(
            Q(
                Q(title__icontains=search_term) | 
                Q(description__icontains=search_term)
            ),
            is_published=True,
        ).order_by('-id')

        return qs 

    def get_context_data(self, *args, **kwargs: Any) -> dict[str, Any]:
        ctx = super().get_context_data(*args, **kwargs)
        search_term = self.get_search_term()
        
        
        ctx.update({
            'page_title': f'Search for "{search_term}"',
            'search_term': search_term,
            'additional_url_query': f'&q={search_term}',
        })

        return ctx


class RecipeDetailViewBase(DetailView):
    model = Recipe
    context_object_name = 'recipe'
    template_name = 'recipes/pages/recipe-view.html'

    def get_queryset(self) -> QuerySet[Recipe]:
        qs = super().get_queryset()
        qs = qs.filter(
            is_published=True
        )

        return qs

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        ctx = super().get_context_data(**kwargs)
        
        ctx.update({
            'is_detail_page': True
        })
        
        return ctx
    
# DetailView API
class RecipeDetailAPI(RecipeDetailViewBase):
    def render_to_response(self, context: dict[str, Any], **response_kwargs: Any) -> HttpResponse:
        recipe = self.get_context_data()['recipe']
        recipe_dict = model_to_dict(recipe)

        recipe_dict['created_at'] = recipe.created_at
        recipe_dict['updated_at'] = recipe.updated_at

        if recipe_dict.get('cover'):
            recipe_dict['cover'] = recipe_dict['cover'].url
        else:
            recipe_dict['cover'] = ''

        del recipe_dict['is_published']
        del recipe_dict['preparation_steps_is_html']

        return JsonResponse(
            recipe_dict,
            safe=False
        )
    

# Teoria
def theory(request, *args, **kwargs):

    # Consulta
    recipes = Recipe.my_manager.get_published()

    context = {
        'recipes': recipes
    }

    return render(
        request, 
        'recipes/pages/theory.html',
        context=context,
    )


class RecipeListViewTag(RecipeListViewBase):
    template_name = 'recipes/pages/tag.html'

    def get_queryset(self, *args, **kwargs) -> QuerySet[Recipe]:
        qs = super().get_queryset(*args, **kwargs)
        qs = qs.filter(tags__slug=self.kwargs.get('slug', ''))

        return qs

    def get_context_data(self, *args, **kwargs: Any) -> dict[str, Any]:
        ctx = super().get_context_data(*args, **kwargs)
        page_title = Tag.objects.filter(slug=self.kwargs.get('slug', '')).first()
        
        if not page_title:
            page_title = 'No recipes found'
        page_title = f'{page_title} - Tag'
        
        ctx.update({
            'page_title': page_title,
        })

        return ctx