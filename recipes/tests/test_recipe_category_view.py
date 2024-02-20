from django.urls import reverse, resolve
from recipes.views import site
from .test_recipe_base import RecipeTestBase
from unittest import skip

class RecipeCategoryViewTest(RecipeTestBase):
    def tearDown(self) -> None:
        return super().tearDown()

    # Verifica se o titulo da receita está presente no conteudo HTML da rota da categoria
    # Neste caso, sempre que é criado uma receita, é criado também uma categoria junto (self.make_recipe())
    # Então tem como passarmos o id da categoria para acessarmos essa URL
    def test_recipe_category_template_loads_recipes(self):
        needed_title = 'This is a category test'
        
        # Need a recipe for this test
        self.make_recipe(needed_title)

        response = self.client.get(reverse('recipes:category', args=(1,)))
        content = response.content.decode('utf-8')

        # Check if one recipe exists
        self.assertIn(needed_title, content)

    # Verifica se a view da URL está funcionando corretamente
    def test_recipe_category_views_function_is_correct(self):
        view = resolve(reverse('recipes:category', kwargs={'category_id': 1000}))
        self.assertIs(view.func.view_class, site.RecipeListViewCategory)

    # Espera retornar 404 caso id da categoria não for encontrado
    def test_recipe_category_view_returns_404_if_no_recipes_found(self):
        response = self.client.get(reverse('recipes:category', kwargs={'category_id': 1000}))
        self.assertEqual(response.status_code, 404)

    # Espera 404 caso receita unica não for encontrada, id nao bate com os dados do bd
    def test_recipe_category_template_dont_load_recipes_not_published(self):
        """Test recipe is_published Falso dont show"""
        # Need a recipe for this test
        recipe = self.make_recipe(is_published=False)

        response = self.client.get(reverse('recipes:recipe', kwargs={'id': recipe.pk}))

        # Check if one recipe exists
        self.assertEqual(response.status_code, 404)