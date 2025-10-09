from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User 
from django.contrib.auth import authenticate, login
import unicodedata

# Create your views here.
def login_view(request):
    print(request.method)
    mensagem = ""
    password = ""
    if request.method == "POST":
        acao = request.POST.get("acao")  # login ou cadastro
        username = request.POST.get("username")
        password = request.POST.get("password")
        special_chars = "!@#$%¨&*()-_=+[{]};:,<.>/?"
        if acao == "cadastro":
            if User.objects.filter(username=username).exists():
                mensagem = "Usuário já existe!"
            elif password is None or password.strip() == "":
                mensagem = "Senha inválida!"      
            elif not any(char in special_chars for char in password):
                mensagem = "Senha deve conter ao menos um caractere especial !@#$%¨&*()-_=+[{]};:,<.>/?"
            elif len(password) < 8:
                mensagem = "Senha deve conter ao menos 8 caracteres!"
            else:
                has_upper = any(unicodedata.category(c) == 'Lu' for c in password)
                if not has_upper:
                    mensagem = "Senha deve conter ao menos uma letra maiúscula!"
                else:
                    User.objects.create_user(username=username, password=password)
                    mensagem = f"Usuário {username} cadastrado com sucesso!"

        elif acao == "login":
            if not User.objects.filter(username=username).exists():
                mensagem = "Usuário não cadastrado."
            else:
                user = authenticate(request, username=username, password=password)
                if user is not None:
                    login(request, user)
                    mensagem = "Login realizado com sucesso!"
                else:
                    mensagem = "Senha incorreta."
    return render(request, 'index.html', {"mensagem": mensagem})
