# Unittest
from unittest.mock import patch
# Django
from django.urls import reverse
# Rest Framework
from rest_framework import test
# Mixins
from recipes.tests.test_recipe_base import RecipeMixin



class RecipeAPIv2TestMixin(RecipeMixin):
    def get_recipe_list_reverse_url(self, reverse_result=None):
        api_url = reverse_result or reverse('recipes:recipes-api-list')

        return api_url


    def get_recipe_api_list(self, reverse_result=None):
        response = self.client.get(self.get_recipe_list_reverse_url(reverse_result)) # type: ignore

        return response
    

    def get_auth_data(self, username, password='1234'):
        userdata = {
            "username": username,
            "password": password
        }
        user = self.make_author(
            username=userdata.get('username'), # type: ignore
            password=userdata.get('password') # type: ignore
        )

        # Cria o token para o usuário
        response = self.client.post(reverse('recipes:token_obtain_pair'), data={**userdata}) # type: ignore
        
        return {
            'jwt_access_token': response.data.get('access'), # type: ignore
            'jwt_refresh_token': response.data.get('refresh'),
            'user': user,
        }
    

    def get_recipe_raw_data(self):
        data = {
            'title': 'This is the title',
            'description': 'This is the description',
            'preparation_time': 1,
            'preparation_time_unit': 'Minutes',
            'servings': 1,
            'servings_unit': 'Porções',
            'preparation_steps': 'This is the preparation steps',
        }

        return data



class RecipeAPIv2Test(test.APITestCase, RecipeAPIv2TestMixin):
    def test_recipe_api_list_returns_status_code_200(self):
        response = self.get_recipe_api_list()
        self.assertEqual(
            response.status_code,
            200
        )


    @patch('recipes.views.api.RecipeAPIV2Pagination.page_size', new=7)
    def test_recipe_api_list_loads_correct_number_of_recipes(self):
        wanted_number_of_recipes = 7
        self.make_recipe_in_batch(qtd=wanted_number_of_recipes)

        response = self.client.get(
            reverse('recipes:recipes-api-list') + '?page=1'
        )
        qtd_of_loaded_recipes = len(response.data.get('results')) # type: ignore

        self.assertEqual(
            wanted_number_of_recipes,
            qtd_of_loaded_recipes
        )


    def test_recipe_api_list_do_not_show_not_published_recipes(self):
        recipes = self.make_recipe_in_batch(qtd=2)
        recipe_not_published = recipes[0]
        recipe_not_published.is_published = False
        recipe_not_published.save()
        response = self.get_recipe_api_list()
        self.assertEqual(
            len(response.data.get('results')), # type: ignore
            1
        )


    @patch('recipes.views.api.RecipeAPIV2Pagination.page_size', new=10)
    def test_recipe_api_list_loads_recipes_by_category_id(self):
        # Creates categories
        category_wanted = self.make_category(name='WANTED_CATEGORY')
        category_not_wanted = self.make_category(name='NOT_WANTED_CATEGORY')

        # Creates 10 recipes
        recipes = self.make_recipe_in_batch(qtd=10)

        # Change all recipes to the wanted category
        for recipe in recipes:
            recipe.category = category_wanted
            recipe.save()

        # Change one recipe to the NOT wanted category
        # As a result, this recipe should NOT show in the page
        recipes[0].category = category_not_wanted
        recipes[0].save()

        # Action: get recipes by wanted category_id
        api_url = reverse('recipes:recipes-api-list') + f'?category_id={category_wanted.id}' # type: ignore
        response = self.get_recipe_api_list(reverse_result=api_url)

        # We should only see recipes from the wanted category
        self.assertEqual(
            len(response.data.get('results')), # type: ignore
            9
        )


    def test_recipe_api_list_user_must_send_jwt_token_to_create_recipe(self):
        # Ação
        api_url = self.get_recipe_list_reverse_url()
        response = self.client.post(api_url)

        # Asserção
        self.assertEqual(
            response.status_code,
            401
        )


    def test_recipe_api_list_logged_user_can_create_a_recipe(self):
        # Ajustes
        recipe_raw_data = self.get_recipe_raw_data()
        auth_data = self.get_auth_data(username='rafael-ribeiro')
        jwt_acess_token = auth_data.get('jwt_access_token')

        # Ação
        response = self.client.post(
            self.get_recipe_list_reverse_url(),
            data=recipe_raw_data,
            HTTP_AUTHORIZATION=f'Bearer {jwt_acess_token}'
        )

        # Asserção
        self.assertEqual(
            response.status_code,
            201
        )


    def test_recipe_api_list_logged_user_can_update_a_recipe(self):
        # Ajustes
        recipe = self.make_recipe()
        
        acess_data = self.get_auth_data(username='test_patch')
        jwt_access_token = acess_data.get('jwt_access_token')
        author = acess_data.get('user')

        recipe.author = author
        recipe.save()

        wanted_new_title = f'The new title updated by {author.username}' # type:ignore

        # Ação
        response = self.client.patch(
            reverse('recipes:recipes-api-detail', args=(recipe.id,)),
            data={
                'title': wanted_new_title
            },
            HTTP_AUTHORIZATION=f'Bearer {jwt_access_token}'
        )

        # Asserção
        self.assertEqual(
            response.data.get('title'), # type: ignore
            wanted_new_title
        )

        self.assertEqual(
            response.status_code,
            200
        )


    def test_recipe_api_list_logged_user_can_update_a_recipe_owned_by_another_user(self):
        # Ajustes
        recipe = self.make_recipe()
        access_data = self.get_auth_data(username='test_patch')
        
        another_user = self.get_auth_data(username='cant_update')
        jwt_access_token_from_another_user = another_user.get('jwt_access_token')
        
        author = access_data.get('user')
        recipe.author = author
        recipe.save()

        # Ação
        response = self.client.patch(
            reverse('recipes:recipes-api-detail', args=(recipe.id,)),
            data={},
            HTTP_AUTHORIZATION=f'Bearer {jwt_access_token_from_another_user}'
        )

        # Asserção
        self.assertEqual(
            response.status_code,
            403
        )