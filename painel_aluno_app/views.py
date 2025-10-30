from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Count, Avg
from django.utils import timezone
from datetime import datetime, timedelta
from .models import (
    Aluno, Turma, Aula, HorarioAula, Frequencia, 
    Aviso, Mensalidade, Mensagem
)
from django.views.decorators.http import require_http_methods
import json


# Create your views here.
@login_required
def painel_aluno(request):
    """Dashboard principal do aluno"""
    try:
        aluno = request.user.aluno
    except Aluno.DoesNotExist:
        return render(request, 'painel_aluno.html', {
            'erro': 'Usuário não está cadastrado como aluno.'
        })
    
    # Buscar turmas do aluno
    turmas = aluno.turmas.filter(ativa=True)
    
    # Buscar avisos recentes (últimos 7 dias)
    data_limite = timezone.now() - timedelta(days=7)
    avisos_recentes = Aviso.objects.filter(
        Q(tipo='GERAL') | 
        Q(turma__in=turmas) | 
        Q(aluno=aluno),
        ativo=True,
        data_criacao__gte=data_limite
    ).distinct().order_by('-importante', '-data_criacao')[:5]
    
    # Buscar próximas aulas (próximos 7 dias)
    hoje = timezone.now().date()
    proximas_aulas = Aula.objects.filter(
        turma__in=turmas,
        data__gte=hoje,
        data__lte=hoje + timedelta(days=7),
        realizada=False
    ).order_by('data', 'hora_inicio')[:5]
    
    # Estatísticas de frequência
    total_aulas = Frequencia.objects.filter(aluno=aluno).count()
    presencas = Frequencia.objects.filter(
        aluno=aluno, 
        status='PRESENTE'
    ).count()
    percentual_presenca = (presencas / total_aulas * 100) if total_aulas > 0 else 0
    
    # Mensalidades pendentes
    mensalidades_pendentes = Mensalidade.objects.filter(
        aluno=aluno,
        status__in=['PENDENTE', 'ATRASADO']
    ).order_by('data_vencimento')[:3]
    
    # Mensagens não lidas
    mensagens_nao_lidas = Mensagem.objects.filter(
        destinatario=request.user,
        lida=False
    ).count()
    
    context = {
        'usuario': request.user,
        'aluno': aluno,
        'turmas': turmas,
        'avisos_recentes': avisos_recentes,
        'proximas_aulas': proximas_aulas,
        'total_aulas': total_aulas,
        'presencas': presencas,
        'percentual_presenca': round(percentual_presenca, 1),
        'mensalidades_pendentes': mensalidades_pendentes,
        'mensagens_nao_lidas': mensagens_nao_lidas,
    }
    
    return render(request, 'painel_aluno.html', context)


@login_required
def horarios_aulas(request):
    """Exibir horários das aulas do aluno"""
    try:
        aluno = request.user.aluno
    except Aluno.DoesNotExist:
        return redirect('painel_aluno')
    
    turmas = aluno.turmas.filter(ativa=True)
    horarios = HorarioAula.objects.filter(turma__in=turmas).order_by('dia_semana', 'hora_inicio')
    
    # Organizar horários por dia da semana
    horarios_por_dia = {}
    for horario in horarios:
        dia = horario.get_dia_semana_display()
        if dia not in horarios_por_dia:
            horarios_por_dia[dia] = []
        horarios_por_dia[dia].append(horario)
    
    context = {
        'usuario': request.user,
        'aluno': aluno,
        'horarios': horarios,
        'horarios_por_dia': horarios_por_dia,
    }
    
    return render(request, 'horarios_aula.html', context)


@login_required
def avisos(request):
    """Listar avisos para o aluno"""
    try:
        aluno = request.user.aluno
    except Aluno.DoesNotExist:
        return redirect('painel_aluno')
    
    turmas = aluno.turmas.filter(ativa=True)
    
    # Buscar todos os avisos relevantes
    avisos_lista = Aviso.objects.filter(
        Q(tipo='GERAL') | 
        Q(turma__in=turmas) | 
        Q(aluno=aluno),
        ativo=True
    ).distinct().order_by('-importante', '-data_criacao')
    
    context = {
        'usuario': request.user,
        'aluno': aluno,
        'avisos': avisos_lista,
    }
    
    return render(request, 'avisos.html', context)


@login_required
def minhas_aulas(request):
    """Listar aulas do aluno com frequência"""
    try:
        aluno = request.user.aluno
    except Aluno.DoesNotExist:
        return redirect('painel_aluno')
    
    turmas = aluno.turmas.filter(ativa=True)
    
    # Buscar aulas realizadas (últimos 30 dias)
    data_limite = timezone.now().date() - timedelta(days=30)
    aulas = Aula.objects.filter(
        turma__in=turmas,
        data__gte=data_limite,
        realizada=True
    ).order_by('-data', '-hora_inicio')
    
    # Adicionar informações de frequência
    aulas_com_frequencia = []
    for aula in aulas:
        try:
            freq = Frequencia.objects.get(aluno=aluno, aula=aula)
            aula.frequencia_status = freq.get_status_display()
            aula.frequencia_obj = freq
        except Frequencia.DoesNotExist:
            aula.frequencia_status = 'Não registrada'
            aula.frequencia_obj = None
        aulas_com_frequencia.append(aula)
    
    context = {
        'usuario': request.user,
        'aluno': aluno,
        'aulas': aulas_com_frequencia,
    }
    
    return render(request, 'minhas_aulas.html', context)


@login_required
def frequencia_aluno(request):
    """Exibir relatório de frequência do aluno"""
    try:
        aluno = request.user.aluno
    except Aluno.DoesNotExist:
        return redirect('painel_aluno')
    
    turmas = aluno.turmas.filter(ativa=True)
    
    # Estatísticas por turma
    estatisticas = []
    for turma in turmas:
        frequencias = Frequencia.objects.filter(aluno=aluno, aula__turma=turma)
        total = frequencias.count()
        presencas = frequencias.filter(status='PRESENTE').count()
        faltas = frequencias.filter(status='FALTA').count()
        faltas_justificadas = frequencias.filter(status='FALTA_JUSTIFICADA').count()
        
        percentual = (presencas / total * 100) if total > 0 else 0
        
        estatisticas.append({
            'turma': turma,
            'total_aulas': total,
            'presencas': presencas,
            'faltas': faltas,
            'faltas_justificadas': faltas_justificadas,
            'percentual_presenca': round(percentual, 1)
        })
    
    context = {
        'usuario': request.user,
        'aluno': aluno,
        'estatisticas': estatisticas,
    }
    
    return render(request, 'frequencia.html', context)


@login_required
def mensalidades_aluno(request):
    """Exibir mensalidades do aluno"""
    try:
        aluno = request.user.aluno
    except Aluno.DoesNotExist:
        return redirect('painel_aluno')
    
    mensalidades = Mensalidade.objects.filter(aluno=aluno).order_by('-mes_referencia')
    
    # Calcular totais
    total_pago = sum(m.valor_final for m in mensalidades if m.status == 'PAGO')
    total_pendente = sum(m.valor_final for m in mensalidades if m.status in ['PENDENTE', 'ATRASADO'])
    
    context = {
        'usuario': request.user,
        'aluno': aluno,
        'mensalidades': mensalidades,
        'total_pago': total_pago,
        'total_pendente': total_pendente,
    }
    
    return render(request, 'mensalidades.html', context)


@login_required
def comunicacao(request):
    """Sistema de mensagens/chat"""
    try:
        aluno = request.user.aluno
    except Aluno.DoesNotExist:
        return redirect('painel_aluno')
    
    # Buscar conversas (mensagens recebidas e enviadas)
    mensagens_recebidas = Mensagem.objects.filter(
        destinatario=request.user
    ).order_by('-data_envio')[:20]
    
    mensagens_enviadas = Mensagem.objects.filter(
        remetente=request.user
    ).order_by('-data_envio')[:20]
    
    context = {
        'usuario': request.user,
        'aluno': aluno,
        'mensagens_recebidas': mensagens_recebidas,
        'mensagens_enviadas': mensagens_enviadas,
    }
    
    return render(request, 'comunicacao.html', context)


@login_required
@require_http_methods(["POST"])
def enviar_mensagem(request):
    """Enviar uma mensagem"""
    try:
        data = json.loads(request.body)
        destinatario_id = data.get('destinatario_id')
        assunto = data.get('assunto', '')
        conteudo = data.get('conteudo')
        
        from django.contrib.auth.models import User
        destinatario = User.objects.get(id=destinatario_id)
        
        mensagem = Mensagem.objects.create(
            remetente=request.user,
            destinatario=destinatario,
            assunto=assunto,
            conteudo=conteudo
        )
        
        return JsonResponse({
            'success': True,
            'mensagem_id': mensagem.id
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'erro': str(e)
        }, status=400)


@login_required
@require_http_methods(["POST"])
def marcar_mensagem_lida(request, mensagem_id):
    """Marcar mensagem como lida"""
    try:
        mensagem = get_object_or_404(Mensagem, id=mensagem_id, destinatario=request.user)
        mensagem.lida = True
        mensagem.data_leitura = timezone.now()
        mensagem.save()
        
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({
            'success': False,
            'erro': str(e)
        }, status=400)


@login_required
def perfil_aluno(request):
    """Exibir e editar perfil do aluno"""
    try:
        aluno = request.user.aluno
    except Aluno.DoesNotExist:
        return redirect('painel_aluno')
    
    if request.method == 'POST':
        # Atualizar dados do perfil
        aluno.telefone = request.POST.get('telefone', aluno.telefone)
        aluno.telefone_emergencia = request.POST.get('telefone_emergencia', aluno.telefone_emergencia)
        aluno.endereco = request.POST.get('endereco', aluno.endereco)
        
        if 'foto' in request.FILES:
            aluno.foto = request.FILES['foto']
        
        aluno.save()
        
        return redirect('perfil_aluno')
    
    context = {
        'usuario': request.user,
        'aluno': aluno,
    }
    
    return render(request, 'perfil_aluno.html', context)