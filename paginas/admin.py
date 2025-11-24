from django.contrib import admin
from django.db.models import Sum, Count, Q
from django.utils.html import format_html
from .models import (
    Aluno, Turma, Aula, HorarioAula, Frequencia, 
    Aviso, Mensalidade, Mensagem, Notificacao,
    Evento, VendaIngresso, ResultadoFinanceiroMensal, DespesaAluno, DespesaAdministrativa
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
        return obj.usuario.get_full_name() or obj.usuario.username
    get_nome_completo.short_description = 'Nome Completo'


@admin.register(HorarioAula)
class HorarioAulaAdmin(admin.ModelAdmin):
    list_display = ['turma', 'dia_semana', 'hora_inicio', 'hora_fim', 'sala']
    list_filter = ['dia_semana', 'turma']
    search_fields = ['turma__nome', 'sala']
    ordering = ['dia_semana', 'hora_inicio']


@admin.register(Aula)
class AulaAdmin(admin.ModelAdmin):
    list_display = ['turma', 'data', 'hora_inicio', 'hora_fim', 'tema', 'realizada', 'tem_video', 'tamanho_video_display']
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
        ('Vídeo da Aula', {
            'fields': ('video', 'data_upload_video'),
            'description': 'Upload de vídeo da aula (máximo 50MB). Formatos: MP4, WebM, AVI, MOV'
        }),
        ('Status', {
            'fields': ('realizada', 'observacoes')
        }),
    )
    
    readonly_fields = ['data_upload_video']
    
    def tem_video(self, obj):
        """Indica se a aula tem vídeo"""
        if obj.video:
            return format_html('<span style="color: green;">✓ Sim</span>')
        return format_html('<span style="color: red;">✗ Não</span>')
    tem_video.short_description = 'Vídeo'
    
    def tamanho_video_display(self, obj):
        """Mostra o tamanho do vídeo"""
        if obj.video:
            tamanho_mb = obj.get_video_size_mb()
            dias = obj.dias_desde_upload()
            cor = 'orange' if dias and dias > 20 else 'green'
            dias_str = f'({dias}d)' if dias else ''
            return format_html(
                '<span style="color: {};">{} MB</span> {}',
                cor,
                f'{tamanho_mb:.1f}',
                dias_str
            )
        return '-'
    tamanho_video_display.short_description = 'Tamanho'
    
    def changelist_view(self, request, extra_context=None):
        """Adiciona estatísticas de vídeos no topo do admin"""
        extra_context = extra_context or {}
        
        # Estatísticas de vídeos
        aulas_com_video = Aula.objects.filter(video__isnull=False).exclude(video='')
        total_videos = aulas_com_video.count()
        
        # Calcular tamanho total (aproximado)
        tamanho_total = sum([aula.get_video_size_mb() for aula in aulas_com_video])
        
        # Vídeos antigos (mais de 30 dias)
        from django.utils import timezone
        data_limite = timezone.now() - timezone.timedelta(days=30)
        videos_antigos = aulas_com_video.filter(data_upload_video__lt=data_limite).count()
        
        extra_context['total_videos'] = total_videos
        extra_context['tamanho_total_mb'] = tamanho_total
        extra_context['tamanho_total_gb'] = tamanho_total / 1024
        extra_context['videos_antigos'] = videos_antigos
        
        return super().changelist_view(request, extra_context=extra_context)


@admin.register(Frequencia)
class FrequenciaAdmin(admin.ModelAdmin):
    list_display = ['aluno', 'aula', 'status_display', 'data_registro']
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
    
    def status_display(self, obj):
        """Mostra o status com cor"""
        cores = {
            'PRESENTE': 'green',
            'FALTA': 'red',
            'FALTA_JUSTIFICADA': 'orange',
            'ATESTADO': 'blue'
        }
        cor = cores.get(obj.status, 'black')
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}</span>',
            cor,
            obj.get_status_display()
        )
    status_display.short_description = 'Status'
    
    def get_urls(self):
        from django.urls import path
        urls = super().get_urls()
        custom_urls = [
            path('registrar-frequencia/', self.admin_site.admin_view(self.registrar_frequencia_view), name='registrar_frequencia'),
            path('registrar-frequencia/<int:aula_id>/', self.admin_site.admin_view(self.registrar_frequencia_aula_view), name='registrar_frequencia_aula'),
        ]
        return custom_urls + urls
    
    def registrar_frequencia_view(self, request):
        """View que lista as aulas para registrar frequência"""
        from django.shortcuts import render
        from django.utils import timezone
        from datetime import timedelta
        
        # Busca aulas dos últimos 30 dias
        data_limite = timezone.now().date() - timedelta(days=30)
        aulas = Aula.objects.filter(data__gte=data_limite).select_related('turma').order_by('-data')
        
        context = {
            **self.admin_site.each_context(request),
            'title': 'Registrar Frequência',
            'aulas': aulas,
            'opts': self.model._meta,
        }
        return render(request, 'admin/frequencia/lista_aulas.html', context)
    
    def registrar_frequencia_aula_view(self, request, aula_id):
        """View que mostra os alunos da aula com checkboxes"""
        from django.shortcuts import render, redirect, get_object_or_404
        from django.contrib import messages
        
        aula = get_object_or_404(Aula, id=aula_id)
        alunos = aula.turma.alunos.all().select_related('usuario').order_by('usuario__first_name')
        
        if request.method == 'POST':
            # Processa o formulário
            for aluno in alunos:
                checkbox_name = f'faltou_{aluno.id}'
                faltou = checkbox_name in request.POST
                
                # Cria ou atualiza a frequência
                frequencia, created = Frequencia.objects.get_or_create(
                    aluno=aluno,
                    aula=aula,
                    defaults={'status': 'FALTA' if faltou else 'PRESENTE'}
                )
                
                if not created:
                    frequencia.status = 'FALTA' if faltou else 'PRESENTE'
                    frequencia.save()
            
            messages.success(request, f'Frequência registrada com sucesso para a aula "{aula}"')
            return redirect('admin:registrar_frequencia')
        
        # Busca frequências já registradas
        frequencias_existentes = {
            f.aluno_id: f.status
            for f in Frequencia.objects.filter(aula=aula)
        }
        
        # Adiciona informação de frequência aos alunos
        alunos_com_frequencia = []
        for aluno in alunos:
            aluno.faltou = frequencias_existentes.get(aluno.id) == 'FALTA'
            alunos_com_frequencia.append(aluno)
        
        context = {
            **self.admin_site.each_context(request),
            'title': f'Registrar Frequência - {aula}',
            'aula': aula,
            'alunos': alunos_com_frequencia,
            'opts': self.model._meta,
        }
        return render(request, 'admin/frequencia/registrar_aula.html', context)
    
    def changelist_view(self, request, extra_context=None):
        """Adiciona botão para registrar frequência"""
        extra_context = extra_context or {}
        extra_context['show_registrar_frequencia'] = True
        return super().changelist_view(request, extra_context)


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


@admin.register(Notificacao)
class NotificacaoAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'tipo', 'titulo', 'data_criacao', 'lida']
    list_filter = ['tipo', 'lida', 'data_criacao']
    search_fields = ['usuario__username', 'titulo', 'mensagem']
    date_hierarchy = 'data_criacao'
    
    fieldsets = (
        ('Destinatário', {
            'fields': ('usuario',)
        }),
        ('Conteúdo', {
            'fields': ('tipo', 'titulo', 'mensagem', 'link')
        }),
        ('Status', {
            'fields': ('lida', 'data_leitura')
        }),
    )
    
    readonly_fields = ['data_leitura']
    
    actions = ['marcar_como_lida']
    
    def marcar_como_lida(self, request, queryset):
        for notificacao in queryset:
            notificacao.marcar_como_lida()
        self.message_user(request, f'{queryset.count()} notificação(ões) marcada(s) como lida(s).')
    marcar_como_lida.short_description = 'Marcar como lida'


@admin.register(Evento)
class EventoAdmin(admin.ModelAdmin):
    list_display = ['nome', 'data_evento', 'valor_ingresso', 'meta_vendas', 'total_vendido_display', 'percentual_meta_display', 'ativo']
    list_filter = ['ativo', 'data_evento']
    search_fields = ['nome', 'descricao', 'local']
    date_hierarchy = 'data_evento'
    list_editable = ['ativo']
    
    fieldsets = (
        ('Informações do Evento', {
            'fields': ('nome', 'descricao', 'imagem')
        }),
        ('Data e Local', {
            'fields': ('data_evento', 'hora_evento', 'local')
        }),
        ('Vendas', {
            'fields': ('valor_ingresso', 'meta_vendas', 'comissao_percentual')
        }),
        ('Status', {
            'fields': ('ativo', 'criado_por')
        }),
    )
    
    def total_vendido_display(self, obj):
        """Mostra total de ingressos vendidos"""
        total = obj.total_vendido()
        cor = 'green' if total >= obj.meta_vendas else 'orange'
        return format_html(
            '<span style="color: {}; font-weight: bold;">{} / {}</span>',
            cor, total, obj.meta_vendas
        )
    total_vendido_display.short_description = 'Vendido / Meta'
    
    def percentual_meta_display(self, obj):
        """Mostra percentual da meta atingido"""
        percentual = obj.percentual_meta()
        if percentual >= 100:
            cor = 'green'
            icone = '✓'
        elif percentual >= 50:
            cor = 'orange'
            icone = '◐'
        else:
            cor = 'red'
            icone = '○'
        
        return format_html(
            '<span style="color: {};">{} {}%</span>',
            cor, icone, f'{percentual:.1f}'
        )
    percentual_meta_display.short_description = 'Progresso'
    
    def save_model(self, request, obj, form, change):
        """Registra quem criou o evento"""
        if not change:
            obj.criado_por = request.user
        super().save_model(request, obj, form, change)


@admin.register(VendaIngresso)
class VendaIngressoAdmin(admin.ModelAdmin):
    list_display = ['evento', 'vendedor_nome', 'quantidade', 'valor_total_display', 'valor_comissao', 'data_venda', 'confirmado']
    list_filter = ['confirmado', 'evento', 'data_venda']
    search_fields = ['evento__nome', 'vendedor__first_name', 'vendedor__last_name', 'vendedor__username']
    date_hierarchy = 'data_venda'
    list_editable = ['confirmado']
    
    fieldsets = (
        ('Venda', {
            'fields': ('evento', 'vendedor', 'quantidade')
        }),
        ('Datas', {
            'fields': ('data_venda', 'data_registro')
        }),
        ('Valores', {
            'fields': ('valor_comissao',),
            'description': 'Calculado automaticamente com base na comissão do evento'
        }),
        ('Status', {
            'fields': ('confirmado', 'observacoes')
        }),
    )
    
    readonly_fields = ['data_registro', 'valor_comissao']
    
    actions = ['confirmar_vendas', 'desconfirmar_vendas']
    
    def vendedor_nome(self, obj):
        """Retorna o nome completo do vendedor"""
        return obj.vendedor.get_full_name() or obj.vendedor.username
    vendedor_nome.short_description = 'Vendedor'
    
    def valor_total_display(self, obj):
        """Mostra o valor total da venda"""
        return format_html(
            '<strong>R$ {}</strong>',
            f'R$ {obj.valor_total():.2f}'
        )
    valor_total_display.short_description = 'Valor Total'
    
    def confirmar_vendas(self, request, queryset):
        """Confirma as vendas selecionadas"""
        count = queryset.update(confirmado=True)
        self.message_user(request, f'{count} venda(s) confirmada(s) com sucesso.')
    confirmar_vendas.short_description = 'Confirmar vendas selecionadas'
    
    def desconfirmar_vendas(self, request, queryset):
        """Remove confirmação das vendas selecionadas"""
        count = queryset.update(confirmado=False)
        self.message_user(request, f'{count} venda(s) marcada(s) como não confirmada(s).')
    desconfirmar_vendas.short_description = 'Desconfirmar vendas selecionadas'


@admin.register(ResultadoFinanceiroMensal)
class ResultadoFinanceiroMensalAdmin(admin.ModelAdmin):
    """
    Admin para gerenciar resultados financeiros mensais.
    Permite inserir, editar e visualizar dados financeiros mês a mês.
    """
    list_display = [
        'mes_formatado_display', 
        'lucro_total_display', 
        'gasto_total_display', 
        'a_receber_total_display',
        'lucro_liquido_display',
        'criado_por',
        'data_atualizacao'
    ]
    
    list_filter = ['mes', 'data_criacao']
    search_fields = ['observacoes']
    date_hierarchy = 'mes'
    readonly_fields = ['data_criacao', 'data_atualizacao', 'criado_por']
    
    fieldsets = (
        ('Período', {
            'fields': ('mes',),
            'description': 'Selecione o primeiro dia do mês de referência (ex: 01/01/2025 para Janeiro/2025)'
        }),
        ('Valores Financeiros', {
            'fields': (
                'lucro_total',
                'gasto_total',
                'a_receber_total'
            ),
            'description': 'Insira os valores em reais (R$)'
        }),
        ('Informações Adicionais', {
            'fields': ('observacoes',),
            'classes': ('collapse',)
        }),
        ('Metadados', {
            'fields': ('criado_por', 'data_criacao', 'data_atualizacao'),
            'classes': ('collapse',)
        }),
    )
    
    def save_model(self, request, obj, form, change):
        """Salva o usuário que criou o registro"""
        if not change:  # Se é um novo registro
            obj.criado_por = request.user
        super().save_model(request, obj, form, change)
    
    def mes_formatado_display(self, obj):
        """Exibe o mês formatado"""
        return obj.mes_formatado()
    mes_formatado_display.short_description = 'Mês/Ano'
    mes_formatado_display.admin_order_field = 'mes'
    
    def lucro_total_display(self, obj):
        """Exibe o lucro total formatado"""
        return format_html(
            '<span style="color: #22c55e; font-weight: bold;">R$ {}</span>',
            f'{obj.lucro_total:,.2f}'.replace(',', 'X').replace('.', ',').replace('X', '.')
        )
    lucro_total_display.short_description = 'Lucro Total'
    
    def gasto_total_display(self, obj):
        """Exibe o gasto total formatado"""
        return format_html(
            '<span style="color: #ef4444; font-weight: bold;">R$ {}</span>',
            f'{obj.gasto_total:,.2f}'.replace(',', 'X').replace('.', ',').replace('X', '.')
        )
    gasto_total_display.short_description = 'Gasto Total'
    
    def a_receber_total_display(self, obj):
        """Exibe o valor a receber formatado"""
        return format_html(
            '<span style="color: #f97316; font-weight: bold;">R$ {}</span>',
            f'{obj.a_receber_total:,.2f}'.replace(',', 'X').replace('.', ',').replace('X', '.')
        )
    a_receber_total_display.short_description = 'A Receber'
    
    def lucro_liquido_display(self, obj):
        """Exibe o lucro líquido formatado com cor baseada no valor"""
        lucro_liquido = obj.lucro_liquido()
        cor = '#22c55e' if lucro_liquido >= 0 else '#ef4444'
        return format_html(
            '<span style="color: {}; font-weight: bold; font-size: 1.1em;">R$ {}</span>',
            cor,
            f'{lucro_liquido:,.2f}'.replace(',', 'X').replace('.', ',').replace('X', '.')
        )
    lucro_liquido_display.short_description = 'Lucro Líquido'


@admin.register(DespesaAluno)
class DespesaAlunoAdmin(admin.ModelAdmin):
    list_display = [
        'aluno', 
        'nome', 
        'categoria_badge', 
        'data_prevista', 
        'valor_previsto_display', 
        'valor_gasto_display',
        'percentual_display',
        'status_badge'
    ]
    list_filter = ['status', 'categoria', 'data_prevista', 'turma']
    search_fields = [
        'aluno__usuario__first_name', 
        'aluno__usuario__last_name',
        'nome',
        'descricao'
    ]
    date_hierarchy = 'data_prevista'
    readonly_fields = ['data_criacao', 'data_atualizacao']
    
    fieldsets = (
        ('Informações Principais', {
            'fields': ('aluno', 'nome', 'descricao', 'categoria', 'turma')
        }),
        ('Valores', {
            'fields': ('valor_previsto', 'valor_gasto', 'status')
        }),
        ('Datas', {
            'fields': ('data_prevista', 'data_pagamento')
        }),
        ('Detalhes Adicionais', {
            'fields': ('observacoes', 'itens'),
            'classes': ('collapse',)
        }),
        ('Metadados', {
            'fields': ('data_criacao', 'data_atualizacao'),
            'classes': ('collapse',)
        }),
    )
    
    def categoria_badge(self, obj):
        cores = {
            'FIGURINO': '#ec4899',  # Rosa
            'VIAGEM': '#3b82f6',    # Azul
            'APRESENTACAO': '#8b5cf6',  # Roxo
            'ACESSORIO': '#f59e0b',  # Amarelo
            'TRANSPORTE': '#10b981',  # Verde
            'ALIMENTACAO': '#ef4444',  # Vermelho
            'HOSPEDAGEM': '#6366f1',  # Indigo
            'MAQUIAGEM': '#ec4899',  # Rosa
            'CABELO': '#f97316',  # Laranja
            'SAPATO': '#8b5cf6',  # Roxo
            'OUTRO': '#6b7280',  # Cinza
        }
        cor = cores.get(obj.categoria, '#6b7280')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 8px; '
            'border-radius: 12px; font-size: 11px; font-weight: bold;">{}</span>',
            cor, obj.categoria_display()
        )
    categoria_badge.short_description = 'Categoria'
    
    def status_badge(self, obj):
        cores = {
            'PLANEJADO': '#f97316',  # Laranja
            'PAGO': '#22c55e',       # Verde
            'PARCIAL': '#eab308',    # Amarelo
            'CANCELADO': '#6b7280',  # Cinza
        }
        cor = cores.get(obj.status, '#6b7280')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 10px; '
            'border-radius: 12px; font-size: 11px; font-weight: bold;">{}</span>',
            cor, obj.status_display()
        )
    status_badge.short_description = 'Status'
    
    def valor_previsto_display(self, obj):
        return format_html(
            '<strong style="color: #6b7280;">R$ {}</strong>',
            f'{obj.valor_previsto:,.2f}'.replace(',', 'X').replace('.', ',').replace('X', '.')
        )
    valor_previsto_display.short_description = 'Valor Previsto'
    
    def valor_gasto_display(self, obj):
        cor = '#22c55e' if obj.esta_dentro_orcamento() else '#ef4444'
        return format_html(
            '<strong style="color: {};">R$ {}</strong>',
            cor,
            f'{obj.valor_gasto:,.2f}'.replace(',', 'X').replace('.', ',').replace('X', '.')
        )
    valor_gasto_display.short_description = 'Valor Gasto'
    
    def percentual_display(self, obj):
        percentual = obj.percentual_gasto()
        if percentual <= 50:
            cor = '#22c55e'  # Verde
        elif percentual <= 100:
            cor = '#eab308'  # Amarelo
        else:
            cor = '#ef4444'  # Vermelho
        
        return format_html(
            '<span style="color: {}; font-weight: bold;">{:.1f}%</span>',
            cor, percentual
        )
    percentual_display.short_description = '% Gasto'


@admin.register(DespesaAdministrativa)
class DespesaAdministrativaAdmin(admin.ModelAdmin):
    """Admin customizado para Despesas Administrativas"""
    
    list_display = [
        'nome', 'categoria_badge', 'fornecedor', 
        'valor_total_display', 'valor_pago_display', 'valor_pendente_display',
        'data_vencimento', 'status_badge', 'criado_por'
    ]
    
    list_filter = [
        'status', 'categoria', 'tipo_pagamento', 
        'forma_pagamento', 'data_vencimento', 'data_criacao'
    ]
    
    search_fields = [
        'nome', 'descricao', 'fornecedor', 
        'numero_documento', 'observacoes'
    ]
    
    date_hierarchy = 'data_vencimento'
    
    readonly_fields = [
        'criado_por', 'data_criacao', 'data_atualizacao',
        'valor_pendente', 'percentual_pago', 'dias_ate_vencimento'
    ]
    
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('nome', 'categoria', 'descricao')
        }),
        ('Fornecedor', {
            'fields': ('fornecedor', 'numero_documento')
        }),
        ('Valores', {
            'fields': (
                ('valor_total', 'valor_pago', 'valor_pendente'),
                'percentual_pago'
            )
        }),
        ('Datas', {
            'fields': (
                ('data_vencimento', 'data_pagamento', 'dias_ate_vencimento'),
            )
        }),
        ('Status e Pagamento', {
            'fields': (
                'status',
                'tipo_pagamento',
                'forma_pagamento'
            )
        }),
        ('Parcelamento', {
            'fields': ('numero_parcelas', 'parcela_atual'),
            'classes': ('collapse',)
        }),
        ('Documentação', {
            'fields': ('comprovante', 'observacoes')
        }),
        ('Metadados', {
            'fields': ('criado_por', 'data_criacao', 'data_atualizacao'),
            'classes': ('collapse',)
        })
    )
    
    def save_model(self, request, obj, form, change):
        """Salvar automaticamente o usuário que criou"""
        if not change:  # Novo objeto
            obj.criado_por = request.user
        super().save_model(request, obj, form, change)
    
    def categoria_badge(self, obj):
        """Exibe categoria com badge colorido"""
        cor = obj.get_categoria_color()
        return format_html(
            '<span style="background-color: {}; color: white; padding: 4px 12px; border-radius: 12px; font-size: 11px; font-weight: bold;">{}</span>',
            cor, obj.categoria_display()
        )
    categoria_badge.short_description = 'Categoria'
    
    def status_badge(self, obj):
        """Exibe status com badge colorido"""
        cor = obj.get_status_color()
        return format_html(
            '<span style="background-color: {}; color: white; padding: 4px 12px; border-radius: 12px; font-size: 11px; font-weight: bold;">{}</span>',
            cor, obj.status_display()
        )
    status_badge.short_description = 'Status'
    
    def valor_total_display(self, obj):
        """Exibe valor total formatado"""
        return format_html(
            '<strong style="color: #6366f1;">R$ {}</strong>',
            f'{obj.valor_total:,.2f}'.replace(',', 'X').replace('.', ',').replace('X', '.')
        )
    valor_total_display.short_description = 'Valor Total'
    
    def valor_pago_display(self, obj):
        """Exibe valor pago formatado"""
        return format_html(
            '<strong style="color: #22c55e;">R$ {}</strong>',
            f'{obj.valor_pago:,.2f}'.replace(',', 'X').replace('.', ',').replace('X', '.')
        )
    valor_pago_display.short_description = 'Valor Pago'
    
    def valor_pendente_display(self, obj):
        """Exibe valor pendente formatado"""
        pendente = obj.valor_pendente()
        cor = '#f59e0b' if pendente > 0 else '#22c55e'
        return format_html(
            '<strong style="color: {};">R$ {}</strong>',
            cor,
            f'{pendente:,.2f}'.replace(',', 'X').replace('.', ',').replace('X', '.')
        )
    valor_pendente_display.short_description = 'Valor Pendente'



