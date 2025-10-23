from django.urls import path
from django.views.generic import RedirectView
from . import views

app_name = 'paginas'

urlpatterns = [
    # Redireciona raiz para home
    path('', RedirectView.as_view(url='/home/', permanent=False), name='root'),
    
    # Home
    path('home/', views.home_view, name='home'),
    
    # Painel do Aluno (estático)
    path('painel/', views.painel_aluno_index, name='painel_index'),
    path('painel/avisos/', views.painel_aluno_avisos, name='painel_avisos'),
    path('painel/horarios/', views.painel_aluno_horarios, name='painel_horarios'),
    path('painel/minhas-aulas/', views.painel_aluno_minhas_aulas, name='painel_minhas_aulas'),
    path('painel/comunicacao/', views.painel_aluno_comunicacao, name='painel_comunicacao'),
    path('painel/chat/', views.painel_aluno_chat, name='painel_chat'),
    
    # Financeiro
    path('financeiro/mensalidades/', views.financeiro_mensalidades, name='financeiro_mensalidades'),
    path('financeiro/extrato/', views.financeiro_extrato, name='financeiro_extrato'),
    path('financeiro/despesas/', views.financeiro_despesas, name='financeiro_despesas'),
    
    # Cadastros
    path('cadastro/aluno/', views.cadastro_aluno, name='cadastro_aluno'),
    path('cadastro/professor/', views.cadastro_professor, name='cadastro_professor'),
    
    # Feedback
    path('feedback/', views.feedback_view, name='feedback'),
]
