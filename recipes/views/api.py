# Django
from django.shortcuts import get_object_or_404
from ..permissions import IsOwner

# Rest Framework
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticatedOrReadOnly

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
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self):
        pk = self.kwargs.get('pk', '')
        obj = get_object_or_404(
            self.get_queryset(),
            pk=pk
        )

        self.check_object_permissions(self.request, obj)

        return obj
    
    def get_permissions(self):
        if self.request.method in ['PATCH', 'DELETE']:
            return [IsOwner(), ]

        return super().get_permissions()
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(author=request.user)
        headers = self.get_success_headers(serializer.data)

        return Response(serializer.data, headers=headers)
    
    def partial_update(self, request, *args, **kwargs):
        recipe = self.get_object()
        serializer = RecipeSerializer(
            instance=recipe,
            data=request.data,
            many=False,
            context={'request': request},
            partial=True
        )
        serializer.is_valid()
        serializer.save()

        return Response(serializer.data)
    

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
    

