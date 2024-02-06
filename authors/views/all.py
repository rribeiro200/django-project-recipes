from django.urls import reverse
from django.http import Http404
from django.shortcuts import redirect, render
from authors.forms import RegisterForm, LoginForm, AuthorRecipeForm
from pprint import pprint
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from recipes.models import Recipe

# Create your views here.
def register_view(request):
    register_form_data = request.session.get('register_form_data', None)
    form = RegisterForm(register_form_data)

    return render(request, 'authors/pages/register_view.html',
        {
            'form': form,
            'form_action': reverse('authors:register_create')
        }
    )

# View responsável somente por TRATAR os DADOS do FORMULÁRIO
def register_create(request):
    if not request.POST:
        raise Http404

    POST = request.POST  # QueryDict com os dados de cada campo do formulário
    request.session['register_form_data'] = POST # Armazenando dados do formulário em uma chave da sessão.
    form = RegisterForm(POST)

    if form.is_valid():
        user = form.save(commit=False)
        user.set_password(user.password) # Salva um password criptografado no BD
        user.save()

        messages.success(request, 'Yor user is created! Please log in.')

        del(request.session['register_form_data'])
        return redirect('authors:login')

    return redirect('authors:register')

def login_view(request):
    form = LoginForm()

    return render(request, 'authors/pages/login.html', 
        {
            'form': form,
            'form_action': reverse('authors:login_create')
        }
    )

def login_create(request):
    
    form = LoginForm(request.POST)
    login_url = reverse('authors:login')

    # Autenticando usuário
    if form.is_valid():
        authenticated_user = authenticate(
            username=form.cleaned_data.get('username', ''),
            password=form.cleaned_data.get('password', ''),
        )

        if authenticated_user is not None:
            messages.success(request, 'Login successfully!')
            login(request, authenticated_user) 
        else:
            messages.error(request, 'Invalid credentials.')
    else:
        messages.error(request, 'Error to validate form data.')

    return redirect(reverse('authors:dashboard'))

@login_required(login_url='authors:login', redirect_field_name='next') # Precisa estar logado para que a view funcione.
def logout_view(request):
    # Tentativa de logout sem estar logado, ou por meio de GET, gera mensagem de erro e Http404
    if not request.POST:
        messages.error(request, 'Invalid logout request')
        raise Http404()
    
    # Redireciona o usuário que tente fazer logout com credenciais diferentes das do usuário atualmente autenticado
    if request.POST.get('username') != request.user.username:
        messages.error(request, 'Invalid logout user')
        return redirect(reverse('authors:login'))
    
    # Se estiver tudo válido, mostra mensagem de logout feito com sucesso
    messages.success(request, 'Logged out successfully')

    # Remove a identificação do usuário autenticado do objeto request e 
    # também remove os dados da sessão associados a esse usuário. O usuário é "desconectado" do sistema.
    logout(request)

    return redirect(reverse('authors:login'))

# View dashboard - área admin do autor
@login_required(login_url='authors:login', redirect_field_name='next')
def dashboard(request):
    # Pegando receitas de um usuário específico e não publicadas
    recipes = Recipe.objects.filter(
        is_published=False, # Receitas não publicadas.
        author=request.user # Dono da receita deve ser o mesmo que está logado no site
    )

    return render(request, 'authors/pages/dashboard.html', 
        {
            'recipes': recipes,
        }
    )

# View para criação de nova receita
@login_required(login_url='authors:login', redirect_field_name='next')
def dashboard_recipe_create(request):
    form = AuthorRecipeForm(  # Formulário de nova receita já recebendo os dados submetidos
        request.POST or None, 
        files=request.FILES or None,
    )

    # Validação e salvamento dos dados do form no banco de dados
    if form.is_valid():
        new_recipe: Recipe = form.save(commit=False)

        new_recipe.author = request.user # Vinculando o usuário logado, como autor da nova receita
        new_recipe.preparation_steps_is_html = False
        new_recipe.is_published = False

        new_recipe.save() # Salvando definitivamente a nova receita no banco de dados
        
        messages.success(request, 'Your new recipe has been created successfully!') # Feedback pro usuário

        return redirect(reverse('authors:dashboard')) # Redirecionando para dashboard de receitas pós cadastro de nova receita

    # Renderizando o template com contexto
    return render(request, 'authors/pages/dashboard_recipe_create.html', 
        {
            'form': form
        }              
    )

# View para deleção de receita
@login_required(login_url='authors:login', redirect_field_name='next')
def dashboard_recipe_delete(request):
    # Requisição só pode ser POST, caso contrário enviará erros para usuário
    if not request.POST:
        raise Http404
    
    # Pegando ID da receita a ser deletada
    recipe_id = request.POST.get('id')

    # Busca a receita especifica
    recipe = Recipe.objects.filter(
        is_published=False,
        author=request.user,
        pk=recipe_id
    ).first()

    if not recipe: # Se não encontrar a receita, lança um 404
        raise Http404
    
    recipe.delete() # Se encontrar a receita, deleta.
    messages.success(request, 'Deleted successfuly!') # Feedback para usuário, receita deletada!

    return redirect(reverse('authors:dashboard')) # Após a ação, usuário volta para dashboard 