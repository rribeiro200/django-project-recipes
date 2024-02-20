from django.db.models.signals import pre_delete
from django.dispatch import receiver
from recipes.models import Recipe
import os

def delete_cover(instance):
    try:
        os.remove(instance.cover.path)
    except (ValueError, FileNotFoundError) as e:
        ...

@receiver(pre_delete, sender=Recipe)
def recipe_cover_delete(sender, instance, *args, **kwargs):
    old_instance = Recipe.my_manager.get(pk=instance.pk)  # Instância pré-deletada
    delete_cover(old_instance)