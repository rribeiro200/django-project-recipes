from django.views import View
from django.http.response import Http404
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from recipes.models import Recipe
from authors.forms import AuthorRecipeForm

# View edição da receita
class DashBoardRecipe(View):
    # Busca receita
    def get_recipe(self, id):
        recipe = None
        # Se receber um id de receita, busca aquela em específico.
        if id:
            # Buscando receita do usuário
            recipe = Recipe.objects.filter(
                is_published=False,
                author=self.request.user, # Autor deve ser o usuário logado
                pk=id
            )
        # Se não existir receita, lança erro pro usuário
        if not recipe:
            messages.error(self.request, 'You do not have recipe for editing')
            raise Http404
        
        return recipe.first() # Retorna a primeira receita achada na base, com base no id
    

    # Renderiza a página HTML para edição ou criação de receitas, fornecendo o formulário necessário.
    def render_recipe(self, form):
        return render(
            self.request,
            'authors/pages/dashboard_recipe.html',
            context={
                'form': form
            }
        )


    # Pegando a requisição GET do usuário
    def get(self, *args, **kwargs):
        recipe = self.get_recipe(kwargs.get('id')) # Método que busca receita
        form = AuthorRecipeForm( # Form para editar dados de uma receita
            instance=recipe
        )
        # Resposta para o usuário - Página com o formulário com a instância da receita que ele clicou
        return self.render_recipe(form)


    # Método para validar formulário
    def validation_form(self, request, recipe_id):
        recipe = self.get_recipe(recipe_id) # Buscando uma instância de receita específica - atualização/criação
        form = AuthorRecipeForm(
            data=request.POST or None, # Novos dados POSTADOS pelo usuário
            files=request.FILES or None, # Arquivos enviados
            instance=recipe # Instancia atual a ser atualizada
        )

        # Validação do formulário para atualização de receita
        if form.is_valid():
            recipe = form.save(commit=False) # Salvamento fake para manipular dados da receita e depois salvar definitivamente
            recipe.author = request.user # Definindo o usuário logado, como autor da receita editada
            recipe.preparation_steps_is_html = False
            recipe.is_published = False
            recipe.save() # Salvando a receita definitivamente após atualização/criação dos campos do form

            # Feedback para usuário
            messages.success(self.request, 'Sua receita foi salva com sucesso!')
            # Retornando o form para ser utilizado no contexto do template
            return form
        

    # Atualização/criação de uma receita, dados POSTADOS pelo usuário
    def post(self, *args, **kwargs):
        recipe_id = kwargs.get('id') # Pegando parametro da URL
        # Validando formulário
        form = self.validation_form(self.request, recipe_id)

        # Resposta para o usuário - Página com o formulário com os dados da receita atualizada.
        return self.render_recipe(form)