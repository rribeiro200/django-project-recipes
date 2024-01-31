from unittest import TestCase
from django.test import TestCase as DjangoTestCase
from authors.forms import RegisterForm
from parameterized import parameterized
from django.urls import reverse

class AuthorRegisterFormUnitTest(TestCase):
    @parameterized.expand([
        ('username', 'Your username'),
        ('email', 'Your e-mail'),
        ('first_name', 'Ex.: John'),
        ('last_name', 'Ex.: Doe1'),
        ('password', 'Type your password'),
        ('password2', 'Repeat your password'),
    ])
    def test_fields_placeholder(self, field, placeholder):
        form = RegisterForm()
        # form.fields['first_name'].widget.attrs['placeholder'] -> 'Ex.: John'
        current_placeholder = form[field].field.widget.attrs['placeholder']

        self.assertEqual(placeholder, current_placeholder)

    @parameterized.expand([
        ('username', 'Obrigatório. 150 caracteres ou menos. Letras, números e @/./+/-/_ apenas.'),
        ('email', 'The e-mail must be valid.'),
        ('password', ('Password must have at least one uppercase letter, '
                      'one lowercase letter and one number. The length should be'
                      'at least 8 characteres'
        )),
    ])
    def test_fields_help_text(self, field, needed):
        form = RegisterForm()
        current = form[field].field.help_text

        self.assertEqual(current, needed)

    @parameterized.expand([
            ('username', 'Username'),
            ('first_name', 'First name'),
            ('last_name', 'Last name'),
            ('email', 'E-mail'),
            ('password', 'Password')
    ])
    def test_field_label(self, field, needed):
        form = RegisterForm()
        current = form[field].label

        self.assertEqual(current, needed)


class AuthorRegisterFormIntegrationTest(DjangoTestCase):
    def setUp(self, *args, **kwargs):
        self.form_data = {
            'username': 'user',
            'first_name': 'first',
            'last_name': 'last',
            'email': 'email@anyemail.com',
            'password': 'Str0ngP@ssword1',
            'password2': 'Str0ngP@ssword2',
        }
        return super().setUp(*args, **kwargs)
    
    
    @parameterized.expand([
        ('username', 'This field must not be empty'),
    ])
    def test_fields_cannot_be_empty(self, field, msg):
        self.form_data[field] = ''
        url = reverse('authors:create')
        response = self.client.post(url, data=self.form_data, follow=True)
        
        self.assertEqual(msg, response.content.decode('utf-8'))