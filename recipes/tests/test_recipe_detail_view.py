from django.urls import reverse, resolve
from recipes.views import site
from .test_recipe_base import RecipeTestBase
from unittest import skip

class RecipeDetailViewTest(RecipeTestBase):
    def tearDown(self) -> None:
        return super().tearDown()

    # Verifica se view de detalhes da receita está funcionando corretamente
    def test_recipe_detail_views_function_is_correct(self):
        view = resolve(reverse('recipes:recipe', kwargs={'id': 1}))
        self.assertIs(view.func, site.recipe)

    # Espera retornar 404 caso id de receita unica nao for encontrado na URL
    def test_recipe_detail_views_returns_404_if_no_recipes_found(self):
        response = self.client.get(reverse('recipes:recipe', kwargs={'id': 1000}))
        self.assertEqual(response.status_code, 404)

    # Verifica se o titulo da receita está presente no conteudo HTML do template renderizado na url de receita unica
    def test_recipe_detail_template_loads_the_correct_recipe(self):
        needed_title = 'This is a detail page'

        self.make_recipe(title=needed_title)

        response = self.client.get(reverse('recipes:recipe', args=(1,)))
        content = response.content.decode('utf-8')

        self.assertIn(needed_title, content)