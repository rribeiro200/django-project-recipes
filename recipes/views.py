from django.shortcuts import render, get_list_or_404, get_object_or_404
from utils.pagination import make_pagination
from utils.recipes.factory import make_recipe
from recipes.models import Recipe, Category
from django.http import Http404, HttpResponse
from django.db.models import Q
from django.core.paginator import Paginator
from django.contrib import messages
import os

PER_PAGE = int(os.environ.get('PER_PAGE', 9))

# Create your views here.
def home(request):
    recipes = Recipe.objects.filter(
            is_published=True,
        ).order_by('-id')
    
    page_obj, pagination_range = make_pagination(request, recipes, PER_PAGE)

    messages.error(request, 'QUE LEGAL, FOI UM SUCESSO!!!')
    messages.success(request, 'QUE LEGAL, FOI UM SUCESSO!!!')
    messages.info(request, 'QUE LEGAL, FOI UM SUCESSO!!!')

    return render(
        request,
        'recipes/pages/home.html',
        context={
            'recipes': page_obj,
            'pagination_range': pagination_range
        }
    )


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