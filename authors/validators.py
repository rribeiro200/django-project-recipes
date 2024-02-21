from django import forms
from recipes.models import Recipe
from utils.strings import is_positive_number
from collections import defaultdict
from django.core.exceptions import ValidationError

# Validação global do formulário de nova receita
class AuthorRecipeValidator():
    def __init__(self, data, errors=None, ErrorClass=None):
        self.data = data
        self.errors = defaultdict(list) if errors is None else errors
        self.ErrorClass = ValidationError if ErrorClass is None else ErrorClass
        self.clean() # Chamando método clean ao instanciar a classe


    # Limpando dados do formulário
    def clean(self, *args, **kwargs):
        self.clean_title()
        self.clean_servings()
        self.clean_preparation_time()

        # Pegando dados limpos do formulário
        cd = self.data
        title = cd.get('title') # Pega o campo de titulo do formulário
        description = cd.get('description') # Campo de descrição do form

        # Validação do campo de description
        if title == description:
            self.errors['title'].append('Cannot be equal to description.')
            self.errors['description'].append('Cannot be equal to title.')

        # Informa o usuário que há erros no formulário
        if self.errors:
            raise self.ErrorClass(self.errors)

    # Validação de um único campo (title)
    def clean_title(self):
        title = self.data.get('title')
        # Validação do campo de título
        if len(title) < 5:
            self.errors['title'].append('Must have at least 5 chars.')

        return title
    
    # Validação de um único campo (preparation_time)
    def clean_preparation_time(self):
        field_name = 'preparation_time'
        field_value = self.data.get(field_name)

        # Caso usuário colocar um número negativo no tempo de preparação da receita
        if not is_positive_number(field_value):
            self.errors[field_name].append('Must be a positive number')

        # Retornar o valor limpo do campo após a validação
        return field_value
    
    # Validação de um único campo (servings)
    def clean_servings(self):
        field_name = 'servings'
        field_value = self.data.get(field_name)

        if not is_positive_number(field_value):
            self.errors[field_name].append('Must be a positive number')

        return field_value