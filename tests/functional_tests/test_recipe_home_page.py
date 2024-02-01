import time
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from utils.browser import make_chrome_browser
from selenium.webdriver.common.by import By

class RecipeHomePageFunctionalTest(StaticLiveServerTestCase):
    def sleep(self, seconds=5):
        time.sleep(seconds)

    def test_the_test(self):
        browser = make_chrome_browser()  # Faz o navegador
        browser.get(self.live_server_url)  # Acessa a minha própria aplicação
        self.sleep()  # Dorme por 5 segundos

        body = browser.find_element(By.TAG_NAME, 'body') # Procura elemento HTML no navegador

        self.assertIn('No recipes found here 🥲', body.text)
        browser.quit()