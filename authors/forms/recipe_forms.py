from django import forms
from recipes.models import Recipe
from utils.django_forms import add_attr
from utils.strings import is_positive_number
from collections import defaultdict
from django.core.exceptions import ValidationError

# Formulário de receitas (edição)
class AuthorRecipeForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs) # Inicia classe pai, antes da classe filha(AuthorRecipeForm)

        self._my_errors = defaultdict(list)

        # Estilizando diretamente campos do formulário
        add_attr(self.fields.get('preparation_steps'), 'class', 'span-2')

    class Meta: # Configurações adicionais deste formulário - metadados
        model = Recipe # Modelo que o formulário está associado
        fields = ('title',  # Quais campos do modelo serão incluídos no formulário 
                  'description', 'preparation_time', 'preparation_time_unit',
                  'servings', 'servings_unit', 'preparation_steps','cover', 'category'
        )
        # Customização e comportamento do elemento (campos do form) para interface de usuário
        widgets = { 
            'cover': forms.FileInput( # Widget usado para campos de arquivo
                attrs={
                    'class': 'span-2'
                }
            ),
            'servings_unit': forms.Select( # Widget usado para campos de escolha
                choices=( # Escolhas
                    ('Porções', 'Porções'),
                    ('Pedaços', 'Pedaços'),
                    ('Pessoas', 'Pessoas'),
                )
            ),
            'preparation_time_unit': forms.Select( # Widget usado para campos de escolha
                choices=( # Escolhas
                    ('Minutos', 'Minutos'),
                    ('Horas', 'Horas'),
                )
            )
        }

    # Limpando dados do formulário
    def clean(self):
        super_clean = super().clean() # Garantindo que a validação da classe pai seja mantida
        
        # Pegando dados limpos do formulário
        cd = self.cleaned_data
        title = cd.get('title') # Pega o campo de titulo do formulário
        description = cd.get('description') # Campo de descrição do form

        # Validação do campo de description
        if title == description:
            self._my_errors['title'].append('Cannot be equal to description.')
            self._my_errors['description'].append('Cannot be equal to title.')

        # Informa o usuário que há erros no formulário
        if self._my_errors:
            raise ValidationError(self._my_errors)

        return super_clean
    
    # Validação de um único campo (title)
    def clean_title(self):
        title = self.cleaned_data.get('title')
        # Validação do campo de título
        if len(title) < 5:
            self._my_errors['title'].append('Must have at least 5 chars.')

        return title
    
    # Validação de um único campo (title)
    def clean_preparation_time(self):
        field_name = 'preparation_time'
        field_value = self.cleaned_data.get(field_name)

        # Caso usuário colocar um número negativo no tempo de preparação da receita
        if not is_positive_number(field_value):
            self._my_errors[field_name].append('Must be a positive number')

        # Retornar o valor limpo do campo após a validação
        return field_value