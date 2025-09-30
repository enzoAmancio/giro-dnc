from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User # ou get_user_model()
from django.contrib.auth import authenticate, login

# Create your views here.
def login_view(request):
    print(request.method)
    mensagem = ""
    if request.method == "POST":
        acao = request.POST.get("acao")  # login ou cadastro
        username = request.POST.get("username")
        password = request.POST.get("password")
        if acao == "cadastro":
            if User.objects.filter(username=username).exists():
                mensagem = "Usuário já existe!"
            else:
                User.objects.create_user(username=username, password=password)
                mensagem = f"Usuário {username} cadastrado com sucesso!"
        elif acao == "login":
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                mensagem = "Login realizado com sucesso!"
            else:
                mensagem = "Usuário ou senha inválidos."
    return render(request, 'login.html', {"mensagem": mensagem})
