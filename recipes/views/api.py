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
@api_view()
def recipe_api_list(request):
    recipes = Recipe.my_manager.get_published()[:10]
    serializer = RecipeSerializer(
        instance=recipes, 
        many=True,
        context={'request': request}
    )

    return Response(serializer.data)


# Visualização de detalhe da receita
@api_view()
def recipe_api_detail(request, pk):
    recipe = Recipe.my_manager.filter(pk=pk).first()

    if recipe:
        serializer = RecipeSerializer(
            instance=recipe, 
            many=False,
            context={'request': request}
        )
        return Response(serializer.data)
    else:
        return Response({
            'detail': 'Eita! Nenhum objeto encontrado.'
        }, status=status.HTTP_418_IM_A_TEAPOT)
    

# Detalhes da tag da receita
@api_view()
def tag_api_detail(request, pk):
    tag = get_object_or_404(Tag.objects.filter(pk=pk))
    serializer = TagSerializer(
        instance=tag, many=False, context={'request': request}
    )

    return Response(serializer.data)