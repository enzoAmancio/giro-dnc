from django.shortcuts import render
from django.views.generic import TemplateView

# Home Page
def home_view(request):
    return render(request, 'home/index.html')

# Painel do Aluno (páginas estáticas HTML puras)
def painel_aluno_index(request):
    return render(request, 'painel/index.html')

def painel_aluno_avisos(request):
    return render(request, 'painel/avisos.html')

def painel_aluno_horarios(request):
    return render(request, 'painel/horarios_aula.html')

def painel_aluno_minhas_aulas(request):
    return render(request, 'painel/minhas_aulas.html')

def painel_aluno_comunicacao(request):
    return render(request, 'painel/comunicacao.html')

def painel_aluno_chat(request):
    return render(request, 'painel/chat.html')

# Financeiro
def financeiro_mensalidades(request):
    return render(request, 'financeiro/mensalidades.html')

def financeiro_extrato(request):
    return render(request, 'financeiro/Extrato.html')

def financeiro_despesas(request):
    return render(request, 'financeiro/despesas.html')

# Cadastros
def cadastro_aluno(request):
    return render(request, 'cadastros/cadastro_aluno_novo.html')

def cadastro_professor(request):
    return render(request, 'cadastros/cadastro_professor_novo.html')

# Feedback
def feedback_view(request):
    return render(request, 'feedback/aba feedback.html')
