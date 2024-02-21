# Django
from django.http import HttpResponse
from django.shortcuts import get_object_or_404

# Rest Framework
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

# Models
from ..models import Recipe
from tag.models import Tag
from ..serializers import RecipeSerializer, TagSerializer


class RecipeAPIV2List(APIView):
    def get(self, request):
        recipes = Recipe.my_manager.get_published()[:10]
        serializer = RecipeSerializer(
            instance=recipes,
            many=True,
            context={'request': request}
        )

        return Response(serializer.data)
        
    def post(self, request):
        serializer = RecipeSerializer(
            data=request.data,
            context={'request': request}
        )
        serializer.is_valid()
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class RecipeAPIV2Detail(APIView):
    def get_recipe(self, pk):
        recipe = get_object_or_404(Recipe.my_manager.get_published(), pk=pk)
        
        return recipe

    def get(self, request, pk):
        recipe = self.get_recipe(pk=pk)
        serializer = RecipeSerializer(
            instance=recipe,
            many=False,
            context={'request': request}
        )

        return Response(serializer.data)
    
    def patch(self, request, pk):
        recipe = self.get_recipe(pk=pk)
        serializer = RecipeSerializer(
            instance=recipe,
            data=request.data,
            many=False,
            context={'request': request},
            partial=True
        )
        serializer.is_valid()
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        recipe = self.get_recipe(pk=pk)
        recipe.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)


# Detalhes de uma TAG de uma receita
@api_view()
def tag_api_detail(request, pk):
    tag = get_object_or_404(Tag.objects.filter(pk=pk))
    serializer = TagSerializer(
        instance=tag, many=False, context={'request': request}
    )

    return Response(serializer.data)