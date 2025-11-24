import os
from django.http import JsonResponse
from django.views.decorators.http import require_GET
from django.views.decorators.csrf import csrf_exempt
from django.utils.dateparse import parse_date
from .models import Aluno, Mensalidade

    
API_TOKEN = os.environ.get("API_EXPORT_TOKEN")
print("=== TOKEN CARREGADO ===", API_TOKEN)
# ---------------------------------------------------------
# EXPORTAÇÃO DE ALUNOS
# ---------------------------------------------------------
@csrf_exempt
@require_GET
def export_alunos(request):
    token = request.GET.get("token")
    if not token or token != API_TOKEN:
        return JsonResponse({"detail": "Unauthorized"}, status=401)

    # Filtros opcionais
    ativo = request.GET.get("ativo")
    if ativo in ["true", "1", "True"]:
        alunos = Aluno.objects.filter(ativo=True)
    elif ativo in ["false", "0", "False"]:
        alunos = Aluno.objects.filter(ativo=False)
    else:
        alunos = Aluno.objects.all()

    data = []
    for a in alunos:
        data.append({
            "id": a.id,
            "nome": a.usuario.get_full_name(),
            "cpf": a.cpf,
            "data_nascimento": a.data_nascimento,
            "telefone": a.telefone,
            "telefone_emergencia": a.telefone_emergencia,
            "endereco": a.endereco,
            "data_matricula": a.data_matricula,
            "ativo": a.ativo,
            "observacoes": a.observacoes,
            "turmas": [t.nome for t in a.turmas.all()],  # lista de nomes da turma
        })

    return JsonResponse(data, safe=False,)

# ---------------------------------------------------------
# EXPORTAÇÃO DE MENSALIDADES
# ---------------------------------------------------------
@csrf_exempt
@require_GET
def export_mensalidades(request):
    token = request.GET.get("token")
    if not token or token != API_TOKEN:
        return JsonResponse({"detail": "Unauthorized"}, status=401)

    qs = Mensalidade.objects.select_related("aluno", "aluno__usuario")

    # Filtro por status
    status = request.GET.get("status")
    if status:
        qs = qs.filter(status=status.upper())

    # Filtro por mês de referência (yyyy-mm)
    mes = request.GET.get("mes")
    if mes:
        qs = qs.filter(mes_referencia__startswith=mes)

    # Filtro por aluno específico
    aluno_id = request.GET.get("aluno_id")
    if aluno_id:
        qs = qs.filter(aluno__id=aluno_id)

    data = []
    from django.utils import timezone
    today = timezone.now().date()

    for m in qs:
        data.append({
            "id": m.id,
            "aluno_id": m.aluno.id,
            "aluno_nome": m.aluno.usuario.get_full_name() or m.aluno.usuario.username,
            "cpf": m.aluno.cpf,

            # Valores
            "mes_referencia": m.mes_referencia,
            "valor": float(m.valor),
            "valor_desconto": float(m.valor_desconto),
            "valor_final": float(m.valor_final),

            # Datas
            "data_vencimento": m.data_vencimento,
            "data_pagamento": m.data_pagamento,

            # Status
            "status": m.status,
            "forma_pagamento": m.forma_pagamento,

            # Atraso
            "dias_em_atraso": m.dias_em_atraso(),

            "observacoes": m.observacoes,
        })

    return JsonResponse(data, safe=False)

