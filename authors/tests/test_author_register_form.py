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
        ('last_name', 'Ex.: Doe'),
        ('password', 'Type your password'),
        ('password2', 'Repeat your password'),
    ])
    def test_fields_placeholder(self, field, placeholder):
        form = RegisterForm()
        # form.fields['first_name'].widget.attrs['placeholder'] -> 'Ex.: John'
        current_placeholder = form[field].field.widget.attrs['placeholder']

        self.assertEqual(placeholder, current_placeholder)

    @parameterized.expand([
        ('username', (
            'Username must have letters, numbers or one of those @.+-_.'
            'The length should be between 4 and 150 characteres.'
        )),
        ('email', 'The e-mail must be valid'),
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
        ('first_name', 'Write your first name'),
        ('last_name', 'Write your last name'),
        ('password', 'Password mus not be empty'),
        ('password2', 'Password and password2 must be equal'),
        ('email', 'E-mail is required'),
    ])
    def test_fields_cannot_be_empty(self, field, msg):
        self.form_data[field] = ''
        url = reverse('authors:create')
        response = self.client.post(url, data=self.form_data, follow=True)
        
        self.assertIn(msg, response.context['form'].errors.get(field))

    def test_username_field_min_length_should_be_4(self):
        self.form_data['username'] = 'd'
        url = reverse('authors:create')
        response = self.client.post(url, data=self.form_data, follow=True)

        msg_error = 'Username must have at least 4 characteres'

        self.assertIn(msg_error, response.context['form'].errors.get('username'))

    def test_username_field_max_length_should_be_150(self):
        self.form_data['username'] = 'A' * 147
        url = reverse('authors:create')
        response = self.client.post(url, data=self.form_data, follow=True)

        msg_error = 'The username must be a maximum of 150 characters.'

        self.assertIn(msg_error, response.context['form'].errors.get('username'))

    def test_password_field_have_lower_upper_case_letters_and_numbers(self):
        self.form_data['password'] = 'Abc12345678'
        url = reverse('authors:create')
        response = self.client.post(url, data=self.form_data, follow=True)

        msg_error = (
            'Password must have at least one uppercase letter, '
            'one lowercase letter and one number.  The length should be'
            'at least 8 characters'
        )
        self.assertIn(msg_error, response.context['form'].errors.get('password'))

    def test_password_and_password_confirmation_are_equal(self):
        self.form_data['password'] = 'Abc12345678'
        self.form_data['password2'] = 'Abc12345678AAAA'
        url = reverse('authors:create')
        response = self.client.post(url, data=self.form_data, follow=True)

        # Se o teste passar, é sinal de que houve este erro no campo password2
        msg_error = 'Password and password2 must be equal'

        self.assertIn(msg_error, response.context['form'].errors.get('password2'))