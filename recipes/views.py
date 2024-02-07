from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render, get_list_or_404, get_object_or_404
from utils.pagination import make_pagination
from utils.recipes.factory import make_recipe
from recipes.models import Recipe, Category
from django.http import Http404, HttpRequest, HttpResponse
from django.db.models import Q
from django.core.paginator import Paginator
import os
from django.views.generic import ListView


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


class RecipeListViewCategory(RecipeListViewBase):
    template_name = 'recipes/pages/category.html'

    def get_queryset(self, *args, **kwargs) -> QuerySet[Recipe]:
        qs = super().get_queryset(*args, **kwargs)
        qs = qs.filter(
            category__id=self.kwargs['category_id'],
            is_published=True
        )
        return qs
    
    def get_context_data(self, *args, **kwargs: Any) -> dict[str, Any]:
        ctx = super().get_context_data(*args, **kwargs)
        object_list = ctx['object_list']
        category_name = object_list[0].category.name
        
        ctx.update({
            'title': f'{category_name} - Category |'
        })
        return ctx


def category(request, category_id):
    recipes = get_list_or_404(
        Recipe.objects.filter(
            category__id=category_id, 
            is_published=True
        ).order_by('-id')
    )
    category_name = recipes[0].category.name  # type: ignore

    page_obj, pagination_range = make_pagination(request, recipes, PER_PAGE)

    return render(
        request,
        'recipes/pages/category.html',
        context={
            'recipes': page_obj,
            'pagination_range': pagination_range,
            'title': f'{category_name} - Category | ',
        }
    )


def recipe(request, id):
    recipe = get_object_or_404(
        Recipe,
        pk=id,
        is_published=True,
    )

    return render(
        request,
        'recipes/pages/recipe-view.html',
        context={
            'recipe': recipe,
            'is_detail_page': True,
        }
    )


def search(request):
    search_term = request.GET.get('q', '').strip()

    if not search_term:
        raise Http404()
    
    recipes = Recipe.objects.filter(
        Q(
            Q(title__icontains=search_term) | 
            Q(description__icontains=search_term)
        ),
        is_published=True,
    ).order_by('-id')

    page_obj, pagination_range = make_pagination(request, recipes, PER_PAGE)

    return render(request, 'recipes/pages/search.html',
        {
            'page_title': f'Search for "{search_term}"',
            'search_term': search_term,
            'recipes': page_obj,
            'pagination_range': pagination_range,
            'additional_url_query': f'&q={search_term}',
        },
    )