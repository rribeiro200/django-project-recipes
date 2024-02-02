import pytest
from .base import AuthorsBaseTest
from django.contrib.auth.models import User
from django.urls import reverse
from selenium.webdriver.common.by import By

@pytest.mark.functional_test
class AuthorLoginTest(AuthorsBaseTest):
    def test_user_valid_data_can_login_successfully(self):
        user = User.objects.create_user(username='username', password='pass')

        # Usuário abre a página de login
        self.browser.get(self.live_server_url + reverse('authors:login'))

        # Obtendo formulário e campos
        form = self.browser.find_element(By.CLASS_NAME, 'main-form')
        username_field = self.get_by_placeholder(form, 'Type your username')
        password_field = self.get_by_placeholder(form, 'Type your password')

        # Logando o usuário
        username_field.send_keys('username')
        password_field.send_keys('pass')
        
        # Submetendo o form
        form.submit()

        # Pegando texto de login feito com sucesso na página
        body = self.browser.find_element(By.TAG_NAME, 'body').text

        # Fim do teste
        self.assertIn('Login successfully!', body)