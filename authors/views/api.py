# Django
from django.shortcuts import get_object_or_404
from recipes.permissions import IsOwner

# Rest Framework
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.permissions import IsAuthenticated

# Models
from ..models import Profile, User
from ..serializers import AuthorSerializer


# View Set - Criação, Listagem, Atualização e Deleção tudo junto
class AuthorViewSet(ReadOnlyModelViewSet):
    serializer_class = AuthorSerializer
    permission_classes = [IsAuthenticated, ]

    def get_queryset(self):
        qs = User.objects.filter(username=self.request.user.username)
        
        return qs