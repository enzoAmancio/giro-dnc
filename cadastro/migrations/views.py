from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.hashers import make_password 
from django.db import IntegrityError 

# Importe todos os seus modelos do models.py
from .models import Aluno, Professor, Atividade 

# -------------------------------------------------------------
# 1. VIEW DE CADASTRO DE ALUNO (Completa)
# -------------------------------------------------------------
def cadastro_aluno(request):
    
    # Dicionário padrão para o template
    context = {
        'page_title': 'Cadastro / Cadastro Aluno',
        'active_page': 'aluno',
        'active_menu': 'cadastro',
        'form_data': {} # Inicialmente vazio
    }
    
    if request.method == 'POST':
        # Armazena todos os dados POST. Usaremos o 'form_data' para preservar o que foi digitado.
        form_data = request.POST 
        context['form_data'] = form_data 

        # --- VALIDAÇÕES DE FRONT-END REPETIDAS NO BACK-END ---
        email = form_data.get('email')
        confirma_email = form_data.get('confirma-email')
        senha = form_data.get('senha')
        confirma_senha = form_data.get('confirma-senha')
        cpf = form_data.get('cpf')

        if email != confirma_email:
            messages.error(request, 'Erro: Os campos de E-mail não coincidem.')
            return render(request, 'cadastro/cadastro_aluno.html', context)
        
        if senha != confirma_senha:
            messages.error(request, 'Erro: Os campos de Senha não coincidem.')
            return render(request, 'cadastro/cadastro_aluno.html', context)
        
        # --- SALVANDO NO BANCO DE DADOS ---
        try:
            # 1. Validação de Unicidade (CPF)
            if Aluno.objects.filter(cpf=cpf).exists():
                messages.error(request, 'Erro: Já existe um aluno cadastrado com este CPF.')
                return render(request, 'cadastro/cadastro_aluno.html', context)
                
            # 2. Criptografa a senha antes de salvar
            senha_hash = make_password(senha)
            
            # 3. Cria o objeto Aluno
            Aluno.objects.create(
                nome_completo=form_data.get('nome'),
                cpf=cpf,
                data_nascimento=form_data.get('nascimento'),
                email=email,
                senha=senha_hash, 
                telefone=form_data.get('telefone'),
                banco=form_data.get('banco'),
                agencia=form_data.get('agencia'),
                conta=form_data.get('conta'),
                titularidade=form_data.get('titularidade')
            )
            
            messages.success(request, f'Aluno(a) {form_data.get("nome")} cadastrado com sucesso!')
            # Redireciona para limpar o formulário e remover os dados POST
            return redirect('cadastro_aluno') 
            
        # Captura erros de banco de dados (ex: E-mail duplicado)
        except IntegrityError:
            messages.error(request, 'Erro: Um aluno com este E-mail ou CPF já está cadastrado.')
            return render(request, 'cadastro/cadastro_aluno.html', context)
            
        except Exception as e:
            # Captura qualquer outro erro inesperado
            messages.error(request, f'Erro inesperado ao cadastrar: {e}')
            return render(request, 'cadastro/cadastro_aluno.html', context)

    # Método GET (Primeira visita ou após um redirect de sucesso)
    return render(request, 'cadastro/cadastro_aluno.html', context)


# -------------------------------------------------------------
# 2. VIEW DE CADASTRO DE PROFESSOR (Para referência)
# -------------------------------------------------------------
def cadastro_professor(request):
    # Lógica de Professor aqui...
    # (É muito similar à de Aluno, mas salvando no modelo Professor)
    pass # Remova este 'pass' e insira o código de Professor.

# -------------------------------------------------------------
# 3. VIEW DE CADASTRO DE ATIVIDADES (Para referência)
# -------------------------------------------------------------
def cadastro_atividades(request):
    # Lógica de Atividades aqui...
    # (Incluindo o tratamento de request.FILES para o upload)
    pass # Remova este 'pass' e insira o código de Atividades.