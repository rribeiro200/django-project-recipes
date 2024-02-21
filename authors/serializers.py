# Utils
from collections import defaultdict
from django.forms import ValidationError
from authors.validators import AuthorRecipeValidator

# Rest Framework
from rest_framework import serializers

# Models
from .models import Profile, User


# Classe Serializadora
class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id', 'username', 'first_name',
            'last_name', 'email',
        ]
    
    def validate(self, attrs):
        super_validate = super().validate(attrs)

        AuthorRecipeValidator(data=attrs, ErrorClass=ValidationError)

        return super_validate