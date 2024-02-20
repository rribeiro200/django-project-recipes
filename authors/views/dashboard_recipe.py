from authors.forms import AuthorRecipeForm
from django.contrib import messages
from django.http.response import Http404
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views import View
from recipes.models import Recipe
from utils.render_template_form_recipe import render_recipe
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

# CRIAR RECEITAS
@method_decorator(
    login_required(login_url='authors:login', redirect_field_name='next'),
    name='dispatch'
)
class DashboardRecipeCreate(View):
    def get(self, request):
        form = AuthorRecipeForm()
        return render_recipe(request, form)

    def post(self, request):
        form = AuthorRecipeForm(
            data=request.POST or None,
            files=request.FILES or None,
        )

        if form.is_valid():
            new_recipe = form.save(commit=False)

            new_recipe.author = request.user
            new_recipe.preparation_steps_is_html = False
            new_recipe.is_published = False
            new_recipe.save()

            messages.success(request, 'Your new recipe has been created successfully!')

            return redirect(reverse('authors:dashboard'))
        
        return render_recipe(request, form)


# EDITAR RECEITAS
@method_decorator(
    login_required(login_url='authors:login', redirect_field_name='next'),
    name='dispatch'
)
class DashboardRecipeEdit(View):
    def get_recipe(self, id=None):
        recipe = None

        if id is not None:
            recipe = Recipe.objects.filter(
                is_published=False,
                author=self.request.user,
                pk=id,
            ).first()

            if not recipe:
                raise Http404()

        return recipe

    def get(self, request, id=None):
        recipe = self.get_recipe(id)
        form = AuthorRecipeForm(instance=recipe)
        return render_recipe(request, form)

    # POST para edição de instância de receita
    def post(self, request, id=None):
        recipe = self.get_recipe(id)
        form = AuthorRecipeForm(
            data=request.POST or None,
            files=request.FILES or None,
            instance=recipe
        )

        if form.is_valid():
            recipe = form.save(commit=False)

            recipe.author = request.user
            recipe.preparation_steps_is_html = False
            recipe.is_published = False

            recipe.save()

            messages.success(request, 'Sua receita foi salva com sucesso!')
            return redirect(
                reverse(
                    'authors:dashboard_recipe_edit', args=(
                        recipe.id,
                    )
                )
            )

        return render_recipe(request, form)
    

# DELETAR RECEITAS
@method_decorator(
    login_required(login_url='authors:login', redirect_field_name='next'),
    name='dispatch'
)
class DashboardRecipeDelete(DashboardRecipeEdit):
    def get(self, request):
        raise Http404

    def post(self, request):
        recipe_id = request.POST.get('id')

        recipe = self.get_recipe(recipe_id)
        recipe.delete() # type: ignore

        messages.success(request, 'Deleted successfully!')
        return redirect(reverse('authors:dashboard'))