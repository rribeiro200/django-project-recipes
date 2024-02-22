# Django
from django.shortcuts import get_object_or_404
from recipes.permissions import IsOwner

# Rest Framework
from rest_framework.response import Response
from rest_framework.decorators import action
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
        qs = User.objects.filter(username=self.request.user.username) # type: ignore
        
        return qs
    

    @action(methods=['get'], detail=False)
    def me(self, request, *args, **kwargs):
        obj = self.get_queryset().first()
        serializer = self.get_serializer(
            instance=obj,
        )

        return Response(serializer.data)