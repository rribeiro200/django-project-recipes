# Django
from django.http import HttpResponse
from django.shortcuts import get_object_or_404

# Rest Framework
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

# Models
from ..models import Recipe
from tag.models import Tag
from ..serializers import RecipeSerializer, TagSerializer


# Paginação
class RecipeAPIV2Pagination(PageNumberPagination):
    page_size = 5


# View Set - Listagem, Criação e Detalhes tudo junto
class RecipeAPIv2ViewSet(ModelViewSet):
    queryset = Recipe.my_manager.get_published()
    serializer_class = RecipeSerializer
    pagination_class = RecipeAPIV2Pagination
    permission_classes = [IsAuthenticated, ]

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
    

