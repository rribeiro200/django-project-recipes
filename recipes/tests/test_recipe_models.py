from .test_recipe_base import RecipeTestBase, Recipe
from django.core.exceptions import ValidationError
from parameterized import parameterized

class RecipeModelTest(RecipeTestBase):
    def setUp(self) -> None:
        self.recipe = self.make_recipe()
        return super().setUp()
    
    def make_recipe_no_defaults(self):
        recipe = Recipe(
            title='Recipe title', description='Recipe description', slug='recipe-slug-2',
            preparation_time=10, preparation_time_unit='Minutos', servings=5, servings_unit='Porções',
            preparation_steps='Recipe preparation_steps', preparation_steps_is_html=False,
            is_published=False, category=self.make_category(name='Teste default cateogry'), author=self.make_author(username='newuser') 
        )
        recipe.full_clean()
        recipe.save()
        return recipe

    # Verificando o max_length de todos os campos do MODEL RECIPE
    @parameterized.expand([
            ('title', 65),
            ('description', 165),
            ('preparation_time_unit', 65),
            ('servings_unit', 65),
        ])
    def test_recipe_fields_max_length(self, field, max_length):
        setattr(self.recipe, field, 'A' * (max_length + 1 ))

        with self.assertRaises(ValidationError):
            self.recipe.full_clean()

    def test_recipe_preparation_steps_is_html_is_false_by_default(self):
        recipe = self.make_recipe_no_defaults()
        self.assertFalse(recipe.preparation_steps_is_html, msg='Recipe preparation_steps_is_html IS NOT FALSE')

    def test_recipe_is_published_is_false_by_default(self):
        recipe = self.make_recipe_no_defaults()
        self.assertFalse(recipe.is_published, msg='Recipe is_published IS NOT FALSE')

    def test_recipe_string_representation(self):
        needed = 'Testing representation'
        self.recipe.title = 'Testing representation'
        self.recipe.full_clean()
        self.recipe.save()
        self.assertEqual(
            str(self.recipe), 
            needed,
            msg=f'Recipe string representation must be' \
                f'"{needed}" but "{str(self.recipe)}" was received'
        )