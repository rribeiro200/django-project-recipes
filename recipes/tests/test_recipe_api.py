# Rest Framework
from rest_framework import test
# Django 
from django.urls import reverse
# Recipes
from recipes.tests.test_recipe_base import RecipeMixin
# Unittest
from unittest.mock import patch


# Classe de teste da API das receitas
class RecipeAPIv2Test(test.APITestCase, RecipeMixin):
    def test_recipe_api_list_returns_status_code_200(self):
        api_url = reverse('recipes:recipes-api-list')
        response = self.client.get(api_url)

        self.assertEqual(response.status_code, 200)


    @patch('recipes.views.api.RecipeAPIV2Pagination.page_size', new=5)
    def test_recipe_api_list_loads_correct_number_of_recipes(self):
        # AJUSTE - Dados que eu quero
        wanted_number_of_recipes = 5
        self.make_recipe_in_batch(wanted_number_of_recipes)

        # AÇÃO
        response = self.client.get(reverse('recipes:recipes-api-list'))
        qtd_recipes_received = response.data.get('results') # type: ignore

        # ASSERÇÃO - Verdade = teste passa, Mentira = teste falha.
        self.assertEqual(
            wanted_number_of_recipes,
            qtd_recipes_received
        )


    def test_(self):
        ...