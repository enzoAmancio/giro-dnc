from rest_framework import serializers
from django.contrib.auth.models import User
from .models import (
    Aluno, Turma, Aula, HorarioAula, Frequencia, 
    Aviso, Mensalidade, Mensagem
)


class UserSerializer(serializers.ModelSerializer):
    """Serializer para o modelo User"""
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']
        read_only_fields = ['id']


class TurmaSerializer(serializers.ModelSerializer):
    """Serializer para o modelo Turma"""
    professor_nome = serializers.CharField(source='professor.get_full_name', read_only=True)
    modalidade_display = serializers.CharField(source='get_modalidade_display', read_only=True)
    nivel_display = serializers.CharField(source='get_nivel_display', read_only=True)
    total_alunos = serializers.SerializerMethodField()
    
    class Meta:
        model = Turma
        fields = [
            'id', 'nome', 'modalidade', 'modalidade_display', 
            'nivel', 'nivel_display', 'professor', 'professor_nome',
            'capacidade_maxima', 'total_alunos', 'ativa', 'descricao',
            'data_inicio', 'data_fim'
        ]
    
    def get_total_alunos(self, obj):
        return obj.alunos.count()


class AlunoSerializer(serializers.ModelSerializer):
    """Serializer para o modelo Aluno"""
    usuario = UserSerializer(read_only=True)
    nome_completo = serializers.CharField(source='usuario.get_full_name', read_only=True)
    turmas = TurmaSerializer(many=True, read_only=True)
    
    class Meta:
        model = Aluno
        fields = [
            'id', 'usuario', 'nome_completo', 'cpf', 'data_nascimento',
            'telefone', 'telefone_emergencia', 'endereco', 'turmas',
            'data_matricula', 'ativo', 'observacoes', 'foto'
        ]
        read_only_fields = ['id', 'data_matricula']


class HorarioAulaSerializer(serializers.ModelSerializer):
    """Serializer para o modelo HorarioAula"""
    turma_nome = serializers.CharField(source='turma.nome', read_only=True)
    dia_semana_display = serializers.CharField(source='get_dia_semana_display', read_only=True)
    
    class Meta:
        model = HorarioAula
        fields = [
            'id', 'turma', 'turma_nome', 'dia_semana', 
            'dia_semana_display', 'hora_inicio', 'hora_fim', 'sala'
        ]


class AulaSerializer(serializers.ModelSerializer):
    """Serializer para o modelo Aula"""
    turma_nome = serializers.CharField(source='turma.nome', read_only=True)
    turma = TurmaSerializer(read_only=True)
    
    class Meta:
        model = Aula
        fields = [
            'id', 'turma', 'turma_nome', 'data', 'hora_inicio',
            'hora_fim', 'tema', 'conteudo', 'realizada', 'observacoes'
        ]


class FrequenciaSerializer(serializers.ModelSerializer):
    """Serializer para o modelo Frequencia"""
    aluno_nome = serializers.CharField(source='aluno.usuario.get_full_name', read_only=True)
    aula_info = AulaSerializer(source='aula', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = Frequencia
        fields = [
            'id', 'aluno', 'aluno_nome', 'aula', 'aula_info',
            'status', 'status_display', 'justificativa', 'data_registro'
        ]
        read_only_fields = ['id', 'data_registro']


class AvisoSerializer(serializers.ModelSerializer):
    """Serializer para o modelo Aviso"""
    autor_nome = serializers.CharField(source='autor.get_full_name', read_only=True)
    tipo_display = serializers.CharField(source='get_tipo_display', read_only=True)
    turma_nome = serializers.CharField(source='turma.nome', read_only=True, allow_null=True)
    
    class Meta:
        model = Aviso
        fields = [
            'id', 'titulo', 'conteudo', 'tipo', 'tipo_display',
            'autor', 'autor_nome', 'turma', 'turma_nome', 'aluno',
            'data_criacao', 'data_expiracao', 'ativo', 'importante'
        ]
        read_only_fields = ['id', 'data_criacao']


class MensalidadeSerializer(serializers.ModelSerializer):
    """Serializer para o modelo Mensalidade"""
    aluno_nome = serializers.CharField(source='aluno.usuario.get_full_name', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = Mensalidade
        fields = [
            'id', 'aluno', 'aluno_nome', 'mes_referencia',
            'valor', 'valor_desconto', 'valor_final',
            'data_vencimento', 'data_pagamento', 'status',
            'status_display', 'forma_pagamento', 'observacoes'
        ]
        read_only_fields = ['id', 'valor_final']


class MensagemSerializer(serializers.ModelSerializer):
    """Serializer para o modelo Mensagem"""
    remetente_nome = serializers.CharField(source='remetente.get_full_name', read_only=True)
    destinatario_nome = serializers.CharField(source='destinatario.get_full_name', read_only=True)
    
    class Meta:
        model = Mensagem
        fields = [
            'id', 'remetente', 'remetente_nome', 'destinatario',
            'destinatario_nome', 'assunto', 'conteudo',
            'data_envio', 'lida', 'data_leitura'
        ]
        read_only_fields = ['id', 'data_envio', 'data_leitura']


class DashboardSerializer(serializers.Serializer):
    """Serializer para dados do dashboard"""
    aluno = AlunoSerializer()
    turmas = TurmaSerializer(many=True)
    avisos_recentes = AvisoSerializer(many=True)
    proximas_aulas = AulaSerializer(many=True)
    total_aulas = serializers.IntegerField()
    presencas = serializers.IntegerField()
    percentual_presenca = serializers.FloatField()
    mensalidades_pendentes = MensalidadeSerializer(many=True)
    mensagens_nao_lidas = serializers.IntegerField()
