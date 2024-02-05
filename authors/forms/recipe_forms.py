from django import forms
from recipes.models import Recipe

# Formulário de receitas (edição)
class AuthorRecipeForm(forms.ModelForm):
    class Meta: # Configurações adicionais deste formulário - metadados
        model = Recipe # Modelo que o formulário está associado
        fields = ('title', 
                  'description', 'preparation_time', 'preparation_time_unit',
                  'servings', 'servings_unit', 'preparation_steps','cover',
        ) # Quais campos do modelo serão incluídos no formulário