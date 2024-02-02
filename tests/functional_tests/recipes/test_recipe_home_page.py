import pytest
from .base import RecipeBaseFunctionalTest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from unittest.mock import patch

@pytest.mark.functional_test
class RecipeHomePageFunctionalTest(RecipeBaseFunctionalTest):
    def test_recipe_home_page_without_recipes_not_found_message(self):
        self.make_recipe_in_batch(qtd=5)
        self.browser.get(self.live_server_url)  # Acessa a minha própria aplicação
        body = self.browser.find_element(By.TAG_NAME, 'body') # Procura elemento HTML no navegador

        self.assertIn('Recipe title', body.text)


    @patch('recipes.views.PER_PAGE', new=2)
    def test_recipe_search_input_can_find_correct_recipes(self):
        recipes = self.make_recipe_in_batch(10)

        title_needed = 'This is what I need'

        recipes[0].title = title_needed
        recipes[0].save()

        # Usuário abre a página
        self.browser.get(self.live_server_url)

        # Vê um campo de busca com o texto "Search for a recipe"
        search_input = self.browser.find_element(
            By.XPATH,
            '//input[@placeholder="Search for a recipe"]'
        )

        # Clica neste input e digita o termo de busca
        # para encontrar a receita o título desejado
        search_input.send_keys(recipes[0].title)
        search_input.send_keys(Keys.ENTER)

        # O usuário vê o que estava procurando no campo de busca
        self.assertIn(
            title_needed,
            self.browser.find_element(By.CLASS_NAME, 'main-content-list').text,
        )
        self.sleep(10)