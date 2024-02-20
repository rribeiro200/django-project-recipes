# Rest Framework
from rest_framework import serializers

# Models
from .models import Category
from django.contrib.auth.models import User
from tag.models import Tag


class TagSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    slug = serializers.CharField()


# Classe Serializadora
class RecipeSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    
    title = serializers.CharField(max_length=65)
    description = serializers.CharField(max_length=165)
    public = serializers.BooleanField(source='is_published')
    preparation = serializers.SerializerMethodField(method_name='get_preparation')
    
    category_id = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())
    category_name = serializers.StringRelatedField(source='category')
    
    author_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    author_name = serializers.StringRelatedField(source='author')

    tags = serializers.PrimaryKeyRelatedField(queryset=Tag.objects.all(), many=True)
    tags_objects = TagSerializer(many=True, source='tags')
    tags_links = serializers.HyperlinkedRelatedField(
        many=True, source='tags', queryset=Tag.objects.all(),
        view_name='recipes:recipes_api_v2_tag'
    )

    def get_preparation(self, recipe):
        return f'{recipe.preparation_time} {recipe.preparation_time_unit}'