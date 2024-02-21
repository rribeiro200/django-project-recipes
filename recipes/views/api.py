# Django
from django.http import HttpResponse
from django.shortcuts import get_object_or_404

# Rest Framework
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, ListCreateAPIView
from rest_framework.pagination import PageNumberPagination

# Models
from ..models import Recipe
from tag.models import Tag
from ..serializers import RecipeSerializer, TagSerializer


# Paginação
class RecipeAPIV2Pagination(PageNumberPagination):
    page_size = 5


# Listagem e Criação
class RecipeAPIV2List(ListCreateAPIView):
    queryset = Recipe.my_manager.get_published()
    serializer_class = RecipeSerializer
    pagination_class = RecipeAPIV2Pagination


# Detalhes
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


# Detalhes
class TagAPIV2Detail(APIView):
    def get(self, request, pk):
        tag = get_object_or_404(Tag.objects.filter(pk=pk))
        serializer = TagSerializer(
            instance=tag,
            many=False,
            context={'request': request}
        )

        return Response(serializer.data)
    

