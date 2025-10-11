from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required


# Create your views here.
@login_required
def painel_aluno(request):
    frequencia = None  # Inicializa a variável frequencia
    try:
        frequencia = request.user.frequencia
    except AttributeError:
        pass  # O usuário não tem um objeto Frequencia associado


    context = {
        'usuario': request.user,
        'frequencia': frequencia,
    }

    return render(request, 'painel_aluno.html', context)