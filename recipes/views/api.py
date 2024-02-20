# Django
from django.http import HttpResponse
from django.shortcuts import get_object_or_404

# Rest Framework
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

# Models
from ..models import Recipe
from ..serializers import RecipeSerializer


# Visualização de lista
@api_view()
def recipe_api_list(request):
    recipes = Recipe.my_manager.get_published()[:10]
    serializer = RecipeSerializer(instance=recipes, many=True)

    return Response(serializer.data)


# Visualização de detalhe
@api_view()
def recipe_api_detail(request, pk):
    recipe = Recipe.my_manager.filter(pk=pk).first()

    if recipe:
        serializer = RecipeSerializer(instance=recipe, many=False)
        return Response(serializer.data)
    else:
        return Response({
            'detail': 'Eita! Nenhum objeto encontrado.'
        }, status=status.HTTP_418_IM_A_TEAPOT)