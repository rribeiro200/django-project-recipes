from django.http import Http404
from django.shortcuts import redirect, render
from authors.forms import RegisterForm
from pprint import pprint
from django.contrib import messages

# Create your views here.
def register_view(request):
    register_form_data = request.session.get('register_form_data', None)
    form = RegisterForm(register_form_data)
    
    # for field in form:

    return render(request, 'authors/pages/register_view.html',
        {
            'form': form
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
        form.save()
        messages.success(request, 'Yor user is created, please log in.')

        del(request.session['register_form_data'])

    return redirect('authors:register')