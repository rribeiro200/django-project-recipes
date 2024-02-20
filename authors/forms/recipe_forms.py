from django import forms
from recipes.models import Recipe
from utils.django_forms import add_attr
from utils.strings import is_positive_number
from collections import defaultdict
from django.core.exceptions import ValidationError
from authors.validators import AuthorRecipeValidator

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
        
        AuthorRecipeValidator(self.cleaned_data, ErrorClass=ValidationError)

        return super_clean