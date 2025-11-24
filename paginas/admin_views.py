"""
Views administrativas personalizadas para gerenciamento do sistema
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.db.models import Q, Count, Sum
from django.utils import timezone
from datetime import timedelta
from calendar import monthrange
from .models import (
    Aluno, Turma, Aula, Frequencia,
    Mensalidade, Evento, Aviso, Mensagem, VendaIngresso
)


def is_superuser(user):
    """Verifica se o usuário é superusuário"""
    return user.is_superuser


@login_required
@user_passes_test(is_superuser)
def admin_dashboard(request):
    """Dashboard administrativo principal"""
    hoje = timezone.now().date()
    mes_atual = hoje.month
    ano_atual = hoje.year
    
    # Pegar filtro de receita (padrão: data_pagamento)
    filtro_receita = request.GET.get('filtro_receita', 'data_pagamento')
    
    # Estatísticas principais
    total_alunos = Aluno.objects.filter(ativo=True).count()
    total_turmas = Turma.objects.filter(ativa=True).count()
    
    # Aulas próximos 7 dias
    aulas_proximos_7_dias = Aula.objects.filter(
        data__gte=hoje,
        data__lte=hoje + timedelta(days=7)
    ).count()
    
    # Receita do mês (baseado no filtro selecionado)
    if filtro_receita == 'mes_referencia':
        receita_mes = Mensalidade.objects.filter(
            mes_referencia__month=mes_atual,
            mes_referencia__year=ano_atual,
            status='PAGO'
        ).aggregate(total=Sum('valor_final'))['total'] or 0
    else:  # data_pagamento
        receita_mes = Mensalidade.objects.filter(
            data_pagamento__month=mes_atual,
            data_pagamento__year=ano_atual,
            status='PAGO'
        ).aggregate(total=Sum('valor_final'))['total'] or 0
    
    # Mensalidades atrasadas
    mensalidades_atrasadas = Mensalidade.objects.filter(
        status='ATRASADO'
    ).select_related('aluno__usuario').order_by('data_vencimento')
    
    # Próximas aulas
    proximas_aulas = Aula.objects.filter(
        data__gte=hoje
    ).select_related('turma').order_by('data', 'hora_inicio')[:10]
    
    # Dados para gráfico de receita (últimos 6 meses)
    receita_labels = []
    receita_valores = []
    meses_pt = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun',
                'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez']
    
    for i in range(5, -1, -1):
        mes = mes_atual - i
        ano = ano_atual
        if mes <= 0:
            mes += 12
            ano -= 1
        
        receita_labels.append(f"{meses_pt[mes-1]}/{str(ano)[2:]}")
        
        if filtro_receita == 'mes_referencia':
            valor = Mensalidade.objects.filter(
                mes_referencia__month=mes,
                mes_referencia__year=ano,
                status='PAGO'
            ).aggregate(total=Sum('valor_final'))['total'] or 0
        else:  # data_pagamento
            valor = Mensalidade.objects.filter(
                data_pagamento__month=mes,
                data_pagamento__year=ano,
                status='PAGO'
            ).aggregate(total=Sum('valor_final'))['total'] or 0
        
        receita_valores.append(float(valor))
    
    # Status de mensalidades
    mens_pagas = Mensalidade.objects.filter(
        mes_referencia__month=mes_atual,
        mes_referencia__year=ano_atual,
        status='PAGO'
    ).count()
    
    mens_pendentes = Mensalidade.objects.filter(
        mes_referencia__month=mes_atual,
        mes_referencia__year=ano_atual,
        status='PENDENTE'
    ).count()
    
    mens_atrasadas = Mensalidade.objects.filter(
        mes_referencia__month=mes_atual,
        mes_referencia__year=ano_atual,
        status='ATRASADO'
    ).count()
    
    context = {
        'total_alunos': total_alunos,
        'total_turmas': total_turmas,
        'aulas_proximos_7_dias': aulas_proximos_7_dias,
        'receita_mes': receita_mes,
        'mensalidades_atrasadas': mensalidades_atrasadas,
        'proximas_aulas': proximas_aulas,
        'receita_labels': receita_labels,
        'receita_valores': receita_valores,
        'mens_pagas': mens_pagas,
        'mens_pendentes': mens_pendentes,
        'mens_atrasadas': mens_atrasadas,
        'filtro_receita': filtro_receita,
    }
    
    return render(request, 'admin_painel/dashboard.html', context)


@login_required
@user_passes_test(is_superuser)
def admin_alunos(request):
    """Gerenciar alunos"""
    alunos = Aluno.objects.select_related('usuario').prefetch_related('turmas').all()
    
    context = {
        'alunos': alunos,
    }
    
    return render(request, 'admin_painel/alunos.html', context)


@login_required
@user_passes_test(is_superuser)
def admin_professores(request):
    """Gerenciar professores (usuários que são professores de turmas)"""
    from django.contrib.auth.models import User
    
    # Busca todos os usuários que são professores de alguma turma
    professores = User.objects.filter(
        turmas_professor__isnull=False
    ).distinct().prefetch_related('turmas_professor')
    
    context = {
        'professores': professores,
    }
    
    return render(request, 'admin_painel/professores.html', context)


@login_required
@user_passes_test(is_superuser)
def admin_turmas(request):
    """Gerenciar turmas"""
    turmas = Turma.objects.prefetch_related('alunos').select_related('professor').all()
    
    context = {
        'turmas': turmas,
    }
    
    return render(request, 'admin_painel/turmas.html', context)


@login_required
@user_passes_test(is_superuser)
def admin_aulas(request):
    """Gerenciar aulas"""
    aulas = Aula.objects.select_related('turma').order_by('-data', '-hora_inicio')
    
    context = {
        'aulas': aulas,
    }
    
    return render(request, 'admin_painel/aulas.html', context)


@login_required
@user_passes_test(is_superuser)
def admin_frequencia_view(request):
    """Gerenciar frequência - redireciona para o admin do Django"""
    return redirect('/admin/paginas/frequencia/registrar-frequencia/')


@login_required
@user_passes_test(is_superuser)
def admin_mensalidades(request):
    """Gerenciar mensalidades"""
    mensalidades = Mensalidade.objects.select_related('aluno__usuario').order_by('-mes_referencia')
    
    # Filtros
    status = request.GET.get('status')
    if status:
        mensalidades = mensalidades.filter(status=status)
    
    context = {
        'mensalidades': mensalidades,
    }
    
    return render(request, 'admin_painel/mensalidades.html', context)


@login_required
@user_passes_test(is_superuser)
def admin_eventos(request):
    """Gerenciar eventos"""
    eventos = Evento.objects.annotate(
        total_vendas=Count('vendas')
    ).order_by('-data_evento')
    
    context = {
        'eventos': eventos,
    }
    
    return render(request, 'admin_painel/eventos.html', context)


@login_required
@user_passes_test(is_superuser)
def admin_vendas_ingressos(request):
    """Ver todas as vendas de ingressos"""
    vendas = VendaIngresso.objects.select_related(
        'evento', 'aluno__usuario'
    ).order_by('-data_venda')
    
    # Estatísticas gerais
    total_ingressos_vendidos = vendas.count()
    total_arrecadado = vendas.aggregate(total=Sum('valor_pago'))['total'] or 0
    
    # Vendas por evento
    vendas_por_evento = Evento.objects.annotate(
        total_vendas=Count('vendas'),
        total_arrecadado=Sum('vendas__valor_pago')
    ).filter(total_vendas__gt=0).order_by('-total_vendas')
    
    context = {
        'vendas': vendas,
        'total_ingressos_vendidos': total_ingressos_vendidos,
        'total_arrecadado': total_arrecadado,
        'vendas_por_evento': vendas_por_evento,
    }
    
    return render(request, 'admin_painel/vendas_ingressos.html', context)


@login_required
@user_passes_test(is_superuser)
def admin_avisos(request):
    """Gerenciar avisos"""
    avisos = Aviso.objects.select_related('autor').order_by('-data_criacao')
    
    context = {
        'avisos': avisos,
    }
    
    return render(request, 'admin_painel/avisos.html', context)


@login_required
@user_passes_test(is_superuser)
def admin_mensagens(request):
    """Gerenciar mensagens"""
    mensagens = Mensagem.objects.select_related('remetente', 'destinatario').order_by('-data_envio')[:50]
    
    context = {
        'mensagens': mensagens,
    }
    
    return render(request, 'admin_painel/mensagens.html', context)


@login_required
@user_passes_test(is_superuser)
def admin_relatorio_financeiro(request):
    """Relatório financeiro completo"""
    hoje = timezone.now().date()
    mes_atual = hoje.month
    ano_atual = hoje.year
    
    # Receita total
    receita_total = Mensalidade.objects.filter(
        status='PAGO'
    ).aggregate(total=Sum('valor_final'))['total'] or 0
    
    # Receita do mês
    receita_mes = Mensalidade.objects.filter(
        mes_referencia__month=mes_atual,
        mes_referencia__year=ano_atual,
        status='PAGO'
    ).aggregate(total=Sum('valor_final'))['total'] or 0
    
    # Inadimplência
    inadimplencia = Mensalidade.objects.filter(
        status='ATRASADO'
    ).aggregate(total=Sum('valor_final'))['total'] or 0
    
    # Mensalidades pendentes
    pendentes = Mensalidade.objects.filter(
        status='PENDENTE'
    ).aggregate(total=Sum('valor_final'))['total'] or 0
    
    context = {
        'receita_total': receita_total,
        'receita_mes': receita_mes,
        'inadimplencia': inadimplencia,
        'pendentes': pendentes,
    }
    
    return render(request, 'admin_painel/relatorio_financeiro.html', context)
