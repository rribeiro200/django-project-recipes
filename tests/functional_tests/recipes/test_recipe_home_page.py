import pytest
from .base import RecipeBaseFunctionalTest
from selenium.webdriver.common.by import By

@pytest.mark.functional_test
class RecipeHomePageFunctionalTest(RecipeBaseFunctionalTest):
    def test_recipe_home_page_without_recipes_not_found_message(self):
        self.browser.get(self.live_server_url)  # Acessa a minha própria aplicação
        body = self.browser.find_element(By.TAG_NAME, 'body') # Procura elemento HTML no navegador

        self.assertIn('No recipes found here 🥲', body.text)