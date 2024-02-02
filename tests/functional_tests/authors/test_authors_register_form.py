from __future__ import annotations
from .base import AuthorsBaseTest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

class AuthorsRegisterTest(AuthorsBaseTest):
    # Pegando o espaço reservado de um campo
    def get_by_placeholder(self, web_element, placeholder):
        return web_element.find_element(
            By.XPATH, f'//input[@placeholder="{placeholder}"]'
        )
    
    # Preenchendo form com dados fakes inválidos
    def fill_form_dummy_data(self, form):
        fields = form.find_elements(By.TAG_NAME, 'input') # Pegando todos os campos do form

        # Para cada campo exibido no form, insere espaços para gerar erros
        for field in fields:
            if field.is_displayed():
                field.send_keys(' ' * 20)


    def test_empty_first_name_error_message(self):
        # Acessa a url de registro de authors
        self.browser.get(self.live_server_url + '/authors/register')
        
        # Busca o formulário da página
        form = self.browser.find_element(
            By.XPATH,
            '/html/body/main/div[2]/form'
        )

        # Preenche form com dados fakes inválidos
        self.fill_form_dummy_data(form)
        # Envia um e-mail fake para o campo do tipo e-mail
        form.find_element(By.NAME, 'email').send_keys('email@email.com')

        # Pega o campo que tem o placeholder desejado
        first_name_field = self.get_by_placeholder(form, 'Ex.: John')
        first_name_field.send_keys(' ') # Envia valores para este campo
        first_name_field.send_keys(Keys.ENTER) # Preciona enter para envio dos dados

        # Anteriormente foi pressionado 'ENTER' no form, então ocorre um REQUEST
        # A partir disso precisamos pegar o formulário novamente:
        form = self.browser.find_element(
            By.XPATH,
            '/html/body/main/div[2]/form'
        )

        # Para o teste passar, o formulário precisa dar erro, e no text precisa conter a mensagem esperada.
        self.assertIn('Write your first name', form.text)