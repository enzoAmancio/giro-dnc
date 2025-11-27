from django.urls import path
from django.views.generic import RedirectView
from . import views
from . import admin_views
from . import api_views

app_name = 'paginas'

urlpatterns = [

    # API Endpoints
    path('api/exportar-alunos/', api_views.export_alunos, name='export_alunos'),
    path('api/exportar-mensalidades/', api_views.export_mensalidades),
    path('api/webhook-mercadopago/', views.webhook_mercadopago, name='webhook_mercadopago'),
    path('financeiro/mensalidade/<int:mensalidade_id>/pagar/',views.pagar_mensalidade,name='pagar_mensalidade'),
    path('financeiro/processar-pagamento/', views.processar_pagamento, name='processar_pagamento'),
    path('api/exportar-frequencias/', api_views.export_frequencias, name='export_frequencias'),
         
    # Redireciona raiz para home
    path('', RedirectView.as_view(url='/home/', permanent=False), name='root'),
    
    # Home
    path('home/', views.home_view, name='home'),
    
    # Página do Sistema
    path('sistema/', views.sistema_view, name='sistema'),
    
    # Autenticação
    path('logout/', views.logout_view, name='logout'),
    
    # Painel do Aluno (estático)
    path('painel/', views.painel_aluno_index, name='painel_index'),
    path('painel/avisos/', views.painel_aluno_avisos, name='painel_avisos'),
    path('painel/horarios/', views.painel_aluno_horarios, name='painel_horarios'),
    path('painel/minhas-aulas/', views.painel_aluno_minhas_aulas, name='painel_minhas_aulas'),
    path('painel/comunicacao/', views.painel_aluno_comunicacao, name='painel_comunicacao'),
    path('painel/chat/', views.painel_aluno_chat, name='painel_chat'),
    
    # Painel Administrativo (apenas superusuários)
    path('admin-painel/', admin_views.admin_dashboard, name='admin_dashboard'),
    path('admin-painel/alunos/', admin_views.admin_alunos, name='admin_alunos'),
    path('admin-painel/professores/', admin_views.admin_professores, name='admin_professores'),
    path('admin-painel/turmas/', admin_views.admin_turmas, name='admin_turmas'),
    path('admin-painel/aulas/', admin_views.admin_aulas, name='admin_aulas'),
    path('admin-painel/frequencia/', admin_views.admin_frequencia_view, name='admin_frequencia'),
    path('admin-painel/mensalidades/', admin_views.admin_mensalidades, name='admin_mensalidades'),
    path('admin-painel/eventos/', admin_views.admin_eventos, name='admin_eventos'),
    path('admin-painel/vendas-ingressos/', admin_views.admin_vendas_ingressos, name='vendas_ingressos'),
    path('admin-painel/avisos/', admin_views.admin_avisos, name='admin_avisos'),
    path('admin-painel/mensagens/', admin_views.admin_mensagens, name='admin_mensagens'),
    path('admin-painel/relatorio-financeiro/', admin_views.admin_relatorio_financeiro, name='admin_relatorio_financeiro'),
    
    # Financeiro
    path('financeiro/mensalidades/', views.financeiro_mensalidades, name='financeiro_mensalidades'),
    path('financeiro/extrato/', views.financeiro_extrato, name='financeiro_extrato'),
    path('financeiro/extrato/csv/', views.financeiro_extrato_csv, name='financeiro_extrato_csv'),
    path('financeiro/despesas/', views.financeiro_despesas, name='financeiro_despesas'),
    
    # Gestão Financeira Mensal (Admin)
    path('financeiro/resultados-mensais/', views.resultados_financeiros, name='resultados_financeiros'),
    path('financeiro/resultados-mensais/exportar/', views.exportar_resultados_excel, name='exportar_resultados_excel'),
    
    # Despesas Pessoais dos Alunos
    path('minhas-despesas/', views.minhas_despesas, name='minhas_despesas'),
    path('minhas-despesas/criar/', views.criar_despesa, name='criar_despesa'),
    path('minhas-despesas/editar/<int:despesa_id>/', views.editar_despesa, name='editar_despesa'),
    path('minhas-despesas/deletar/<int:despesa_id>/', views.deletar_despesa, name='deletar_despesa'),
    
    # Despesas Administrativas (Admin)
    path('despesas-admin/', views.despesas_administrativas, name='despesas_administrativas'),
    path('despesas-admin/criar/', views.criar_despesa_admin, name='criar_despesa_admin'),
    path('despesas-admin/editar/<int:despesa_id>/', views.editar_despesa_admin, name='editar_despesa_admin'),
    path('despesas-admin/deletar/<int:despesa_id>/', views.deletar_despesa_admin, name='deletar_despesa_admin'),
    path('despesas-admin/exportar/', views.exportar_despesas_admin_excel, name='exportar_despesas_admin_excel'),
    
    # Cadastros
    path('cadastro/aluno/', views.cadastro_aluno, name='cadastro_aluno'),
    path('cadastro/professor/', views.cadastro_professor, name='cadastro_professor'),
    
    # Feedback
    path('feedback/', views.feedback_view, name='feedback'),
    
    # API Endpoints
    path('api/enviar-mensagem/', views.enviar_mensagem, name='enviar_mensagem'),
    path('api/grafico-frequencia/', views.grafico_frequencia, name='grafico_frequencia'),
    path('api/notificacoes/', views.listar_notificacoes, name='listar_notificacoes'),
    path('api/notificacoes/<int:notificacao_id>/lida/', views.marcar_notificacao_lida, name='marcar_notificacao_lida'),
    path('api/contato-consultor/', views.contato_consultor, name='contato_consultor'),
    
    # Eventos e Vendas de Ingressos
    path('eventos/', views.eventos_lista, name='eventos_lista'),
    path('eventos/<int:evento_id>/', views.evento_detalhes, name='evento_detalhes'),
    path('eventos/<int:evento_id>/registrar-venda/', views.registrar_venda, name='registrar_venda'),
    path('minhas-vendas/', views.minhas_vendas, name='minhas_vendas'),
    path('admin/eventos-dashboard/', views.admin_eventos_dashboard, name='admin_eventos_dashboard'),
]
