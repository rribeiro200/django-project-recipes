from django.urls import reverse, resolve
from recipes import views
from .test_recipe_base import RecipeTestBase
from unittest import skip

class RecipeHomeViewTest(RecipeTestBase):
    def tearDown(self) -> None:
        return super().tearDown()

    # Verifica se a view está correspondendo corretamente ao acessar HOME
    def test_recipe_home_views_function_correct(self):
        view = resolve(reverse('recipes:home'))
        self.assertIs(view.func, views.home)

    # Verifica se status_code ao acessar HOME é 200 OK
    def test_recipe_home_view_returns_status_code_200_OK(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertEqual(response.status_code, 200)

    # Verifica se o template ao acessar HOME está correto
    def test_recipe_home_view_loads_correct_template(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertTemplateUsed(response, 'recipes/pages/home.html')

    # Verificando se no HTML do template HOME existe o conteudo (texto exibido quando não há receitas)
    @skip('WIP')
    def test_recipe_home_template_shows_no_recipes_found_if_no_recipes(self):
        response = self.client.get(reverse('recipes:home'))
        html_response_string = response.content.decode('utf-8')
        self.assertIn(
            'No recipes found here 🥲',
            html_response_string
        )

        # Tenho que escrever mais algumas coisas sobre o teste
        self.fail('Para que eu termine de digitá-lo')

    # Verifica se tem TÍTULO da receita no conteudo do template renderizado em HOME, com base no CONTEXTO da VIEW
    def test_recipe_home_template_loads_recipes(self):
        # Need a recipe for this test
        self.make_recipe()

        response = self.client.get(reverse('recipes:home'))
        content = response.content.decode('utf-8')
        response_context_recipes = response.context['recipes']

        # Check if one recipe exists
        self.assertIn('Recipe title', content)

    # Verifica se aparece texto de atenção caso receita tem atributo is_published=False
    def test_recipe_home_template_dont_load_recipes_not_published(self):
        """Test recipe is_published Falso dont show"""
        # Need a recipe for this test
        self.make_recipe(is_published=False)

        response = self.client.get(reverse('recipes:home'))
        content = response.content.decode('utf-8')

        # Check if one recipe exists
        self.assertIn(
            '<h1>No recipes found here 🥲</h1>',
            content,
        )