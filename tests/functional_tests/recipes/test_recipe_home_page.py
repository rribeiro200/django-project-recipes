import pytest
from typing import List
from .base import RecipeBaseFunctionalTest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from unittest.mock import patch
from recipes.models import Recipe

@pytest.mark.functional_test
class RecipeHomePageFunctionalTest(RecipeBaseFunctionalTest):
    def test_recipe_home_page_without_recipes_not_found_message(self) -> None:
        self.make_recipe_in_batch(qtd=5)
        self.browser.get(self.live_server_url)  # Acessa a minha própria aplicação
        body = self.browser.find_element(By.TAG_NAME, 'body') # Procura elemento HTML no navegador

        self.assertIn('Recipe title', body.text)


    @patch('recipes.views.PER_PAGE', new=2)
    def test_recipe_search_input_can_find_correct_recipes(self) -> None:
        recipes: List[Recipe] = self.make_recipe_in_batch(10)

        title_needed: str = 'This is what I need'

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

    @patch('recipes.views.PER_PAGE', new=2)
    def test_home_page_pagination(self):
        self.make_recipe_in_batch()

        # Usuário abre a página
        self.browser.get(self.live_server_url)

        # Vê que tem uma paginação e clica na página 2
        page2 = self.browser.find_element(
            By.XPATH,
            '//a[@aria-label="Go to page 2"]'
        )
        page2.click()

        # Verifica quantos elementos tem na página 2 (depois do click no link que leva até ela.)
        element_list_length = len(self.browser.find_elements(By.CLASS_NAME, 'recipe'))

        # Vê que tem mais 2 receitas na página 2
        self.assertEqual(element_list_length, 2)

        self.sleep(10)