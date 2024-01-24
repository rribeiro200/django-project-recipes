from django.contrib import admin
from recipes.models import Category, Receipe

# Register your models here.
class CategoryAdmin(admin.ModelAdmin):
    ...

@admin.register(Receipe)
class RecipeAdmin(admin.ModelAdmin):
    ...

admin.site.register(Category, CategoryAdmin)