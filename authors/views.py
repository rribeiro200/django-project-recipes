from django.urls import reverse
from django.http import Http404
from django.shortcuts import redirect, render
from authors.forms import RegisterForm, LoginForm
from pprint import pprint
from django.contrib import messages

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

        messages.success(request, 'Yor user is created, please log in.')

        del(request.session['register_form_data'])

    return redirect('authors:register')


def login_view(request):

    form = LoginForm(request.POST)

    return render(request, 'authors/pages/login.html', 
        {
            'form': form,
            'form_action': reverse('authors:login')
        }
    )


def login_create(request):
    return render(request, 'authors/pages/login.html')