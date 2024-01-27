from django.contrib import admin
from recipes.models import Category, Recipe

# Register your models here.
class CategoryAdmin(admin.ModelAdmin):
    ...

@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'author',)

admin.site.register(Category, CategoryAdmin)