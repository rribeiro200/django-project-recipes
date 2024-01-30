from django import forms
from django.contrib.auth.models import User

def add_attr(field, attr_name, attr_val):
    # Valor atual do atributo do campo. Retorna vazio, se não existe aquele atributo para aquele campo
    existing_attr = field.widget.attrs.get(attr_name, '')
    field.widget.attrs[attr_name] = f'{existing_attr} {attr_val}'.strip()


def add_placeholder(field, placeholder_val):
    field.widget.attrs['placeholder'] = placeholder_val


class RegisterForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        add_placeholder(self.fields['username'], 'Your username')
        add_placeholder(self.fields['email'], 'Your e-mail')

    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Your password'
        })
    )

    password2 = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Repeat your password'
        })
    )

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'username',
            'email',
            'password',
        ]
        labels = {
            'username': 'Username',
            'first_name': 'First name',
            'last_name': 'Last name',
            'email': 'E-mail',
            'password': 'Password',
        }
        help_texts = {
            'email': 'The e-mail must be valid.',
        }
        error_messages = {
            'username': {
                'required': 'This field must not be empty',
            }
        }
        widgets = {
            'username': forms.TextInput(attrs={
                'placeholder': 'Type your username here',
                'class': 'input text-input outra-classe'
            }),
            'password': forms.PasswordInput(attrs={
                'placeholder': 'Type your password here'
            })
        }