from django.db.models.signals import pre_delete, pre_save
from django.dispatch import receiver
from recipes.models import Recipe
import os

# Apaga caminho do cover
def delete_cover(instance):
    try:
        os.remove(instance.cover.path)
    except (ValueError, FileNotFoundError) as e:
        ...

# Apagando um cover do diretório da aplicação
@receiver(pre_delete, sender=Recipe)
def recipe_cover_delete(sender, instance, *args, **kwargs):
    old_instance = Recipe.my_manager.get(pk=instance.pk)  # Instância pré-deletada
    delete_cover(old_instance)


# Depois de atualizar o cover, apagando o caminho do antigo cover.
@receiver(pre_save, sender=Recipe)
def recipe_cover_update(sender, created, instance, *args, **kwargs):
    old_instance = Recipe.my_manager.get(pk=instance.pk)
    is_new_cover = old_instance.cover != instance.cover

    if is_new_cover:
        delete_cover(old_instance)