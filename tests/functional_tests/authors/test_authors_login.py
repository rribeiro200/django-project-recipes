import pytest
from .base import AuthorsBaseTest
from django.contrib.auth.models import User
from django.urls import reverse
from selenium.webdriver.common.by import By

@pytest.mark.functional_test
class AuthorLoginTest(AuthorsBaseTest):
    def test_user_valid_data_can_login_successfully(self):
        # Criando um novo usuário fictício para este teste
        string_password = 'pass'
        user = User.objects.create_user(username='username', password=string_password)

        # Usuário abre a página de login
        self.browser.get(self.live_server_url + reverse('authors:login'))

        # Obtendo formulário e campos
        form = self.browser.find_element(By.CLASS_NAME, 'main-form')
        username_field = self.get_by_placeholder(form, 'Type your username')
        password_field = self.get_by_placeholder(form, 'Type your password')

        # Logando o usuário
        username_field.send_keys(user.username)
        password_field.send_keys(string_password)
        
        # Submetendo o form
        form.submit()

        # Pegando texto de login feito com sucesso na página
        body = self.browser.find_element(By.TAG_NAME, 'body').text

        # Fim do teste
        self.assertIn('Login successfully!', body)

    def test_login_create_raises_404_if_not_POST_method(self):
        self.browser.get(self.live_server_url + reverse('authors:login_create'))

        body = self.browser.find_element(By.TAG_NAME, 'body').text

        self.assertIn('Not Found', body) 

    def test_form_login_is_invalid(self):
        # Abre a página de login
        self.browser.get(self.live_server_url + reverse('authors:login'))

        # Obtendo o form
        form = self.browser.find_element(By.CLASS_NAME, 'main-form')

        # Enviando valores inválidos (vazios) nos campos obtidos
        username = self.get_by_placeholder(form, 'Type your username')
        password = self.get_by_placeholder(form, 'Type your password')
        username.send_keys(' ')
        password.send_keys(' ')

        # Enviando o form
        form.submit()

        # Pegando o texto da página
        body = self.browser.find_element(By.TAG_NAME, 'body').text

        # Vê mensagem de erro na tela
        self.assertIn('Error to validate form data.', body)

    def test_form_login_invalid_credentials(self):
        # Abre a página de login
        self.browser.get(self.live_server_url + reverse('authors:login'))

        # Obtendo o form
        form = self.browser.find_element(By.CLASS_NAME, 'main-form')

        # Enviando valores inválidos - dados que nao correspondem à o que tem na base
        username = self.get_by_placeholder(form, 'Type your username')
        password = self.get_by_placeholder(form, 'Type your password')
        username.send_keys('invalid_user')
        password.send_keys('invalid_password')

        # Enviando o form
        form.submit()

        # Pegando o texto da página
        body = self.browser.find_element(By.TAG_NAME, 'body').text

        # Vê mensagem de erro na tela
        self.assertIn('Invalid credentials.', body)
