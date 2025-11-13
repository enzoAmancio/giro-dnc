from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User 
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import ensure_csrf_cookie
from django.contrib import messages
import unicodedata
import re

# Create your views here.
@ensure_csrf_cookie
def login_view(request):
    print(f"Method: {request.method}")
    print(f"CSRF Cookie: {request.COOKIES.get('csrftoken', 'NOT FOUND')}")
    print(f"CSRF Token from POST: {request.POST.get('csrfmiddlewaretoken', 'NOT FOUND')}")
    
    mensagem = ""
    
    if request.method == "POST":
        acao = request.POST.get("acao")  # login ou cadastro
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "")
        
        # Validações básicas
        if not username:
            mensagem = "Nome de usuário é obrigatório!"
            return render(request, 'login.html', {"mensagem": mensagem})
        
        if not password:
            mensagem = "Senha é obrigatória!"
            return render(request, 'login.html', {"mensagem": mensagem})
        
        # Validar caracteres especiais no username
        if not re.match(r'^[\w.@+-]+$', username):
            mensagem = "Nome de usuário contém caracteres inválidos!"
            return render(request, 'login.html', {"mensagem": mensagem})
        
        special_chars = "!@#$%¨&*()-_=+[{]};:,<.>/?"
        
        if acao == "cadastro":
            # Validações de cadastro
            if len(username) < 3:
                mensagem = "Nome de usuário deve ter pelo menos 3 caracteres!"
            elif len(username) > 150:
                mensagem = "Nome de usuário muito longo (máximo 150 caracteres)!"
            elif User.objects.filter(username=username).exists():
                mensagem = "Usuário já existe!"
            elif len(password) < 8:
                mensagem = "Senha deve conter ao menos 8 caracteres!"
            elif len(password) > 128:
                mensagem = "Senha muito longa (máximo 128 caracteres)!"
            elif not any(char in special_chars for char in password):
                mensagem = "Senha deve conter ao menos um caractere especial !@#$%¨&*()-_=+[{]};:,<.>/?"
            else:
                has_upper = any(unicodedata.category(c) == 'Lu' for c in password)
                has_lower = any(unicodedata.category(c) == 'Ll' for c in password)
                has_digit = any(c.isdigit() for c in password)
                
                if not has_upper:
                    mensagem = "Senha deve conter ao menos uma letra maiúscula!"
                elif not has_lower:
                    mensagem = "Senha deve conter ao menos uma letra minúscula!"
                elif not has_digit:
                    mensagem = "Senha deve conter ao menos um número!"
                else:
                    try:
                        User.objects.create_user(username=username, password=password)
                        mensagem = f"Usuário {username} cadastrado com sucesso! Faça login para continuar."
                        messages.success(request, mensagem)
                    except Exception as e:
                        mensagem = f"Erro ao criar usuário: {str(e)}"
                        messages.error(request, mensagem)

        elif acao == "login":
            if not User.objects.filter(username=username).exists():
                mensagem = "Usuário não cadastrado."
            else:
                user = authenticate(request, username=username, password=password)
                if user is not None:
                    # Verificar se usuário está ativo
                    if not user.is_active:
                        mensagem = "Sua conta está desativada. Entre em contato com o administrador."
                    else:
                        login(request, user)
                        print(f"✅ Login bem-sucedido para: {username}")
                        print(f"   User autenticado: {request.user.is_authenticated}")
                        print(f"   Session key: {request.session.session_key}")
                        
                        # Salva explicitamente a sessão
                        request.session.save()
                        
                        # Redireciona para o painel do aluno autenticado
                        next_url = request.GET.get('next', 'paginas:painel_index')
                        print(f"   Redirecionando para: {next_url}")
                        return redirect(next_url)
                else:
                    mensagem = "Senha incorreta."
            
    return render(request, 'login.html', {"mensagem": mensagem})

def logout_view(request):
    """View para fazer logout do usuário"""
    logout(request)
    messages.info(request, "Você saiu do sistema com sucesso.")
    return redirect('/login/')

print ("login/views.py carregado")