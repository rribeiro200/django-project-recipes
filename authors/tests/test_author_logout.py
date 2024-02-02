from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse

class AuthorLogoutTest(TestCase):
    """ CONTINUAR TRABALHANDO NESTE TESTE EM ESPECÍFICO """
    def test_user_tries_to_logout_using_get_method(self):
        User.objects.create_user(username='my_user', password='my_pass')
        self.client.login(username='my_user', password='my_pass')

        response = self.client.get(
            reverse('authors:logout'),
            follow=True
        )

        self.assertIn(
            'Invalid logout request',
            response.content.decode('utf-8')
        )

    def test_user_tries_to_logout_another_user(self):
        # Criando um usuario ficticio para o teste
        User.objects.create_user(username='my_user', password='pass')
        # Simulando o login de um usuário
        self.client.login(username='my_user', password='pass')

        # Obtendo conteúdo de resposta pós logout do usuário
        response = self.client.post(
            reverse('authors:logout'), 
            data={'username': 'another_user'},
            follow=True
        )
        content_response = response.content.decode('utf-8')

        self.assertIn('Invalid logout user', content_response)

    def test_user_logout_successfully(self):
        # Criando um usuario ficticio para o teste
        User.objects.create_user(username='my_user', password='pass')
        # Simulando o login de um usuário
        self.client.login(username='my_user', password='pass')

        # Fazendo logout com tudo válido (POST e CREDENCIAIS), e obtendo conteúdo de resposta pós logout do usuário
        response = self.client.post(
            reverse('authors:logout'), 
            data={'username': 'my_user'}, # Passando o mesmo username que está logado/autenticado
            follow=True
        )
        content_response = response.content.decode('utf-8')

        self.assertIn('Logged out successfully', content_response)