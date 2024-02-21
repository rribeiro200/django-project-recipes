# Django
from django.http import HttpResponse
from django.shortcuts import get_object_or_404

# Rest Framework
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

# Models
from ..models import Recipe
from tag.models import Tag
from ..serializers import RecipeSerializer, TagSerializer


# Visualização de lista de receitas
@api_view(http_method_names=['get', 'post'])
def recipe_api_list(request):
    if request.method == 'GET':
        recipes = Recipe.my_manager.get_published()[:10]
        serializer = RecipeSerializer(
            instance=recipes, 
            many=True,
            context={'request': request}
        )
        
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = RecipeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)


# Visualização de detalhe de uma receita
@api_view(http_method_names=['get', 'patch', 'delete'])
def recipe_api_detail(request, pk):
    recipe = get_object_or_404(
        Recipe.my_manager.get_published(), pk=pk
    )

    if request.method == 'GET':
        serializer = RecipeSerializer(
            instance=recipe,
            many=False,
            context={'request': request}
        )

        return Response(serializer.data)
    elif request.method == 'PATCH':
        serializer = RecipeSerializer(
            instance=recipe,
            data=request.data,
            many=False,
            context={'request': request},
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)
    elif request.method == 'DELETE':
        recipe.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)


# Detalhes da tag da receita
@api_view()
def tag_api_detail(request, pk):
    tag = get_object_or_404(Tag.objects.filter(pk=pk))
    serializer = TagSerializer(
        instance=tag, many=False, context={'request': request}
    )

    return Response(serializer.data)