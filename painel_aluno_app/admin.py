from django.contrib import admin
from .models import (
    Aluno, Turma, Aula, HorarioAula, Frequencia, 
    Aviso, Mensalidade, Mensagem
)


@admin.register(Turma)
class TurmaAdmin(admin.ModelAdmin):
    list_display = ['nome', 'modalidade', 'nivel', 'professor', 'capacidade_maxima', 'ativa']
    list_filter = ['modalidade', 'nivel', 'ativa']
    search_fields = ['nome', 'professor__first_name', 'professor__last_name']
    list_editable = ['ativa']
    date_hierarchy = 'data_inicio'
    
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('nome', 'modalidade', 'nivel', 'professor')
        }),
        ('Configurações', {
            'fields': ('capacidade_maxima', 'ativa', 'descricao')
        }),
        ('Período', {
            'fields': ('data_inicio', 'data_fim')
        }),
    )


@admin.register(Aluno)
class AlunoAdmin(admin.ModelAdmin):
    list_display = ['get_nome_completo', 'cpf', 'telefone', 'data_matricula', 'ativo']
    list_filter = ['ativo', 'data_matricula', 'turmas']
    search_fields = ['usuario__first_name', 'usuario__last_name', 'cpf', 'telefone']
    list_editable = ['ativo']
    date_hierarchy = 'data_matricula'
    filter_horizontal = ['turmas']
    
    fieldsets = (
        ('Usuário', {
            'fields': ('usuario', 'foto')
        }),
        ('Dados Pessoais', {
            'fields': ('cpf', 'data_nascimento')
        }),
        ('Contato', {
            'fields': ('telefone', 'telefone_emergencia', 'endereco')
        }),
        ('Turmas', {
            'fields': ('turmas',)
        }),
        ('Status', {
            'fields': ('ativo', 'observacoes')
        }),
    )
    
    def get_nome_completo(self, obj):
        return obj.usuario.get_full_name()
    get_nome_completo.short_description = 'Nome Completo'


@admin.register(HorarioAula)
class HorarioAulaAdmin(admin.ModelAdmin):
    list_display = ['turma', 'dia_semana', 'hora_inicio', 'hora_fim', 'sala']
    list_filter = ['dia_semana', 'turma']
    search_fields = ['turma__nome', 'sala']
    ordering = ['dia_semana', 'hora_inicio']


@admin.register(Aula)
class AulaAdmin(admin.ModelAdmin):
    list_display = ['turma', 'data', 'hora_inicio', 'hora_fim', 'tema', 'realizada']
    list_filter = ['realizada', 'data', 'turma']
    search_fields = ['turma__nome', 'tema']
    list_editable = ['realizada']
    date_hierarchy = 'data'
    
    fieldsets = (
        ('Turma e Horário', {
            'fields': ('turma', 'data', 'hora_inicio', 'hora_fim')
        }),
        ('Conteúdo', {
            'fields': ('tema', 'conteudo')
        }),
        ('Status', {
            'fields': ('realizada', 'observacoes')
        }),
    )


@admin.register(Frequencia)
class FrequenciaAdmin(admin.ModelAdmin):
    list_display = ['aluno', 'aula', 'status', 'data_registro']
    list_filter = ['status', 'aula__data', 'aula__turma']
    search_fields = ['aluno__usuario__first_name', 'aluno__usuario__last_name']
    date_hierarchy = 'aula__data'
    
    fieldsets = (
        ('Aluno e Aula', {
            'fields': ('aluno', 'aula')
        }),
        ('Status', {
            'fields': ('status', 'justificativa')
        }),
    )


@admin.register(Aviso)
class AvisoAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'tipo', 'autor', 'data_criacao', 'importante', 'ativo']
    list_filter = ['tipo', 'importante', 'ativo', 'data_criacao']
    search_fields = ['titulo', 'conteudo']
    list_editable = ['importante', 'ativo']
    date_hierarchy = 'data_criacao'
    
    fieldsets = (
        ('Conteúdo', {
            'fields': ('titulo', 'conteudo', 'tipo')
        }),
        ('Destinatários', {
            'fields': ('turma', 'aluno'),
            'description': 'Deixe em branco para aviso geral'
        }),
        ('Configurações', {
            'fields': ('autor', 'importante', 'ativo', 'data_expiracao')
        }),
    )


@admin.register(Mensalidade)
class MensalidadeAdmin(admin.ModelAdmin):
    list_display = ['aluno', 'mes_referencia', 'valor', 'valor_final', 'data_vencimento', 'status']
    list_filter = ['status', 'mes_referencia', 'data_vencimento']
    search_fields = ['aluno__usuario__first_name', 'aluno__usuario__last_name']
    date_hierarchy = 'mes_referencia'
    
    fieldsets = (
        ('Aluno e Período', {
            'fields': ('aluno', 'mes_referencia')
        }),
        ('Valores', {
            'fields': ('valor', 'valor_desconto', 'valor_final'),
            'description': 'O valor final é calculado automaticamente'
        }),
        ('Pagamento', {
            'fields': ('data_vencimento', 'data_pagamento', 'status', 'forma_pagamento')
        }),
        ('Observações', {
            'fields': ('observacoes',)
        }),
    )
    
    readonly_fields = ['valor_final']


@admin.register(Mensagem)
class MensagemAdmin(admin.ModelAdmin):
    list_display = ['remetente', 'destinatario', 'assunto', 'data_envio', 'lida']
    list_filter = ['lida', 'data_envio']
    search_fields = ['remetente__username', 'destinatario__username', 'assunto', 'conteudo']
    date_hierarchy = 'data_envio'
    
    fieldsets = (
        ('Participantes', {
            'fields': ('remetente', 'destinatario')
        }),
        ('Mensagem', {
            'fields': ('assunto', 'conteudo')
        }),
        ('Status', {
            'fields': ('lida', 'data_leitura')
        }),
    )
    
    readonly_fields = ['data_leitura']
