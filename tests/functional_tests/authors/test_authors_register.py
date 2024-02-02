import pytest
from .base import AuthorsBaseTest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

@pytest.mark.functional_test
class AuthorsRegisterTest(AuthorsBaseTest):
    # Preenchendo form com dados fakes inválidos
    def fill_form_dummy_data(self, form):
        fields = form.find_elements(By.TAG_NAME, 'input') # Pegando todos os campos do form
        # Para cada campo exibido no form, insere espaços para gerar erros
        for field in fields:
            if field.is_displayed():
                field.send_keys(' ' * 20)

    # Obtém o formulário
    def get_form(self):
        return self.browser.find_element(By.XPATH, 'html/body/main/div[2]/form')
    
    def form_field_test_with_callback(self, callback):
        # Acessa a url de registro de authors
        self.browser.get(self.live_server_url + '/authors/register')
        
        # Busca o formulário da página
        form = self.get_form()

        # Preenche form com dados fakes inválidos
        self.fill_form_dummy_data(form)
        # Envia um e-mail fake para o campo do tipo e-mail
        form.find_element(By.NAME, 'email').send_keys('email@email.com')

        # Função em que ocorre a asserção do teste, contento a mensagem esperada, no text do form
        callback(form)

        return form

    def test_empty_first_name_error_message(self):
        def callback(self, form):
            # Pega o campo com base no placeholder passado como parametro
            first_name_field = self.get_by_placeholder(form, 'Ex.: John')
            first_name_field.send_keys(' ') # Envia valores(em branco) para este campo
            first_name_field.send_keys(Keys.ENTER) # Preciona enter para envio dos dados do form

            # Anteriormente foi pressionado 'ENTER' no form, então ocorre um REQUEST
            # A partir disso precisamos pegar o formulário novamente:
            form = self.get_form()

            # Para o teste passar, o formulário precisa dar erro, e no text precisa conter a mensagem esperada.
            self.assertIn('Write your first name', form.text)
        
        # Chama a função que executa um callback que valida se a asserção do formulário ocorreu.
        self.form_field_test_with_callback(callback)

    def test_empty_last_name_error_message(self):
        def callback(form):
            last_name_field = self.get_by_placeholder(form, 'Ex.: Doe')
            last_name_field.send_keys(' ')
            last_name_field.send_keys(Keys.ENTER)

            form = self.get_form()

            self.assertIn('Write your last name', form.text)
        self.form_field_test_with_callback(callback)

    def test_empty_username_error_message(self):
        def callback(form):
            last_name_field = self.get_by_placeholder(form, 'Your username')
            last_name_field.send_keys(' ')
            last_name_field.send_keys(Keys.ENTER)

            form = self.get_form()

            self.assertIn('This field must not be empty', form.text)
        self.form_field_test_with_callback(callback)

    def test_empty_email_error_message(self):
        def callback(form):
            last_name_field = self.get_by_placeholder(form, 'Your e-mail')
            last_name_field.send_keys(' ')
            last_name_field.send_keys(Keys.ENTER)

            form = self.get_form()

            self.assertIn('E-mail is required', form.text)
        self.form_field_test_with_callback(callback)

    def test_passwords_do_not_match(self):
        def callback(form):
            password1 = self.get_by_placeholder(form, 'Type your password')
            password2 = self.get_by_placeholder(form, 'Repeat your password')
            password1.send_keys(' 1')
            password2.send_keys(' 2')
            password2.send_keys(Keys.ENTER)

            form = self.get_form()

            self.assertIn('Password and password2 must be equal', form.text)
        self.form_field_test_with_callback(callback)


    def test_user_valid_data_register_successfully(self):
        # Acessa a url do formulário de registo de authors
        self.browser.get(self.live_server_url + '/authors/register')
        # Pega o form HTML
        form = self.get_form()

        # Seleciona o campo no form com base no placeholder, e manda/digita um valor nele
        self.get_by_placeholder(form, 'Ex.: John').send_keys('First Name')
        self.get_by_placeholder(form, 'Ex.: Doe').send_keys('Last Name')
        self.get_by_placeholder(form, 'Your username').send_keys('my_username')
        self.get_by_placeholder(form, 'Your e-mail').send_keys('email@email.com.br')
        self.get_by_placeholder(form, 'Type your password').send_keys('Abc12345678')
        self.get_by_placeholder(form, 'Repeat your password').send_keys('Abc12345678')

        # Envio do formulário
        form.submit()

        # Pegando o body da página após envio do form com dados válidos
        body = self.browser.find_element(By.TAG_NAME, 'body')

        self.assertIn('Yor user is created! Please log in', body.text)