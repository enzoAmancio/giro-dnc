from django.urls import path
from . import views

app_name = 'painel_aluno_app'

urlpatterns = [
    # Dashboard principal
    path('', views.painel_aluno, name='painel_aluno'),
    
    # Horários de aulas
    path('horarios/', views.horarios_aulas, name='horarios_aulas'),
    
    # Avisos
    path('avisos/', views.avisos, name='avisos'),
    
    # Minhas aulas
    path('minhas-aulas/', views.minhas_aulas, name='minhas_aulas'),
    
    # Frequência
    path('frequencia/', views.frequencia_aluno, name='frequencia_aluno'),
    
    # Mensalidades
    path('mensalidades/', views.mensalidades_aluno, name='mensalidades_aluno'),
    
    # Comunicação/Chat
    path('comunicacao/', views.comunicacao, name='comunicacao'),
    path('mensagem/enviar/', views.enviar_mensagem, name='enviar_mensagem'),
    path('mensagem/<int:mensagem_id>/ler/', views.marcar_mensagem_lida, name='marcar_mensagem_lida'),
    
    # Perfil
    path('perfil/', views.perfil_aluno, name='perfil_aluno'),
]
