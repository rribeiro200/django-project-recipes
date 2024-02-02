import time
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from utils.browser import make_chrome_browser
from selenium.webdriver.common.by import By

class AuthorsBaseTest(StaticLiveServerTestCase):
    # Todos os testes se iniciarão com essas configurações:
    def setUp(self) -> None:
        # Atributo com um browser Chrome já configurado com (Options, Service e WebDriver)
        self.browser = make_chrome_browser()
        return super().setUp()
    
    # Todos os testes ao serem finalizados fecharam o navegador e desliga o executável ChromiumDriver
    def tearDown(self) -> None:
        self.browser.quit()
        return super().tearDown()
    
    def sleep(self, qtd=10):
        time.sleep(qtd)

    # Pegando o espaço reservado de um campo de formulário
    def get_by_placeholder(self, web_element, placeholder):
        return web_element.find_element(
            By.XPATH, f'//input[@placeholder="{placeholder}"]'
        )