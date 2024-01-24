from django.shortcuts import render, get_list_or_404, get_object_or_404
from utils.recipes.factory import make_recipe
from recipes.models import Recipe, Category
from django.http import Http404, HttpResponse

# Create your views here.
def home(request):
    recipes = Recipe.objects.all().filter(is_published=True).order_by('-id')
    return render(
        request,
        'recipes/pages/home.html',
        context={
            'recipes': recipes,
        }
    )


def category(request, category_id):
    recipes = get_list_or_404(
        Recipe.objects.filter(
            category__id=category_id, 
            is_published=True
        ).order_by('-id')
    )
    category_name = recipes[0].category.name

    return render(
        request,
        'recipes/pages/category.html',
        context={
            'recipes': recipes,
            'title': f'{category_name} - Category | ',
        }
    )


def recipe(request, id):
    recipe = Recipe.objects.filter(
        pk=id,
        is_published=True,
    ).order_by('-id').first()

    return render(
        request,
        'recipes/pages/recipe-view.html',
        context={
            'recipe': recipe,
            'is_detail_page': True,
        }
    )