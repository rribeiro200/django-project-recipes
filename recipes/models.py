from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=65, null=True)

    def __str__(self):
        return self.name

class Receipe(models.Model):
    title = models.CharField(max_length=65, null=True)
    description = models.CharField(max_length=165, null=True)
    slug = models.SlugField(null=True)
    preparation_time = models.IntegerField(null=True)
    preparation_time_unit = models.CharField(max_length=65, null=True)
    servings = models.IntegerField(null=True)
    servings_unit = models.CharField(max_length=65, null=True)
    preparation_steps = models.TextField(null=True)
    preparation_steps_is_html = models.BooleanField(default=False, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    is_published = models.BooleanField(default=False, null=True)
    cover = models.ImageField(upload_to='recipes/covers/%Y/%m/%d', null=True)
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True
    )
    author = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True
    )

    def __str__(self):
        return self.title