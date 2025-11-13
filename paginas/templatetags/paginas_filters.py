from django import template
from datetime import datetime

register = template.Library()

@register.filter
def format_status(status):
    """Formata o status da mensalidade com cores"""
    status_colors = {
        'PAGO': 'success',
        'PENDENTE': 'warning',
        'ATRASADO': 'danger',
        'CANCELADO': 'secondary'
    }
    return status_colors.get(status, 'secondary')

@register.filter
def format_frequencia(status):
    """Formata o status da frequência com cores"""
    status_colors = {
        'PRESENTE': 'success',
        'FALTA': 'danger',
        'FALTA_JUSTIFICADA': 'warning',
        'ATESTADO': 'info'
    }
    return status_colors.get(status, 'secondary')

@register.filter
def mes_nome(date):
    """Retorna o nome do mês em português"""
    if not date:
        return ''
    meses = [
        'Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho',
        'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro'
    ]
    return meses[date.month - 1]

@register.filter
def dia_semana(date):
    """Retorna o dia da semana em português"""
    if not date:
        return ''
    dias = ['Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta', 'Sábado', 'Domingo']
    return dias[date.weekday()]

@register.filter
def calcular_percentual(valor, total):
    """Calcula percentual"""
    if not total or total == 0:
        return 0
    return round((valor / total) * 100, 1)

@register.filter
def dias_ate_vencimento(data_vencimento):
    """Calcula quantos dias faltam para o vencimento"""
    if not data_vencimento:
        return None
    hoje = datetime.now().date()
    delta = (data_vencimento - hoje).days
    return delta

@register.filter
def is_atrasado(data_vencimento):
    """Verifica se está atrasado"""
    if not data_vencimento:
        return False
    return datetime.now().date() > data_vencimento

@register.filter
def truncate_chars(value, arg):
    """Trunca string no número de caracteres especificado"""
    if len(value) > arg:
        return value[:arg] + '...'
    return value

@register.filter
def get_item(dictionary, key):
    """Acessa um item do dicionário pela chave"""
    return dictionary.get(key)
