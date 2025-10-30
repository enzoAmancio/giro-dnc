from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.utils import timezone
from datetime import timedelta
from django.db.models import Q

from .models import (
    Aluno, Turma, Aula, HorarioAula, Frequencia, 
    Aviso, Mensalidade, Mensagem
)
from .serializers import (
    AlunoSerializer, TurmaSerializer, AulaSerializer, 
    HorarioAulaSerializer, FrequenciaSerializer, AvisoSerializer,
    MensalidadeSerializer, MensagemSerializer, DashboardSerializer
)


class AlunoViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet para Alunos (somente leitura)
    """
    queryset = Aluno.objects.all()
    serializer_class = AlunoSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        # Aluno só vê seus próprios dados
        user = self.request.user
        if hasattr(user, 'aluno'):
            return Aluno.objects.filter(id=user.aluno.id)
        return Aluno.objects.none()
    
    @action(detail=False, methods=['get'])
    def me(self, request):
        """Retorna os dados do aluno logado"""
        try:
            aluno = request.user.aluno
            serializer = self.get_serializer(aluno)
            return Response(serializer.data)
        except Aluno.DoesNotExist:
            return Response(
                {'erro': 'Usuário não está cadastrado como aluno'},
                status=status.HTTP_404_NOT_FOUND
            )
    
    @action(detail=False, methods=['get'])
    def dashboard(self, request):
        """Retorna dados do dashboard do aluno"""
        try:
            aluno = request.user.aluno
            turmas = aluno.turmas.filter(ativa=True)
            
            # Avisos recentes
            data_limite = timezone.now() - timedelta(days=7)
            avisos_recentes = Aviso.objects.filter(
                Q(tipo='GERAL') | 
                Q(turma__in=turmas) | 
                Q(aluno=aluno),
                ativo=True,
                data_criacao__gte=data_limite
            ).distinct().order_by('-importante', '-data_criacao')[:5]
            
            # Próximas aulas
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
            
            data = {
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
            
            serializer = DashboardSerializer(data)
            return Response(serializer.data)
            
        except Aluno.DoesNotExist:
            return Response(
                {'erro': 'Usuário não está cadastrado como aluno'},
                status=status.HTTP_404_NOT_FOUND
            )


class TurmaViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet para Turmas (somente leitura)
    """
    queryset = Turma.objects.filter(ativa=True)
    serializer_class = TurmaSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        # Aluno só vê suas turmas
        user = self.request.user
        if hasattr(user, 'aluno'):
            return user.aluno.turmas.filter(ativa=True)
        return Turma.objects.none()


class AulaViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet para Aulas (somente leitura)
    """
    queryset = Aula.objects.all()
    serializer_class = AulaSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        if hasattr(user, 'aluno'):
            turmas = user.aluno.turmas.filter(ativa=True)
            return Aula.objects.filter(turma__in=turmas).order_by('-data', '-hora_inicio')
        return Aula.objects.none()
    
    @action(detail=False, methods=['get'])
    def proximas(self, request):
        """Retorna as próximas aulas do aluno"""
        try:
            aluno = request.user.aluno
            turmas = aluno.turmas.filter(ativa=True)
            hoje = timezone.now().date()
            
            proximas_aulas = Aula.objects.filter(
                turma__in=turmas,
                data__gte=hoje,
                realizada=False
            ).order_by('data', 'hora_inicio')[:10]
            
            serializer = self.get_serializer(proximas_aulas, many=True)
            return Response(serializer.data)
        except Aluno.DoesNotExist:
            return Response(
                {'erro': 'Usuário não está cadastrado como aluno'},
                status=status.HTTP_404_NOT_FOUND
            )


class HorarioAulaViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet para Horários de Aulas (somente leitura)
    """
    queryset = HorarioAula.objects.all()
    serializer_class = HorarioAulaSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        if hasattr(user, 'aluno'):
            turmas = user.aluno.turmas.filter(ativa=True)
            return HorarioAula.objects.filter(turma__in=turmas).order_by('dia_semana', 'hora_inicio')
        return HorarioAula.objects.none()


class FrequenciaViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet para Frequências (somente leitura)
    """
    queryset = Frequencia.objects.all()
    serializer_class = FrequenciaSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        if hasattr(user, 'aluno'):
            return Frequencia.objects.filter(aluno=user.aluno).order_by('-aula__data')
        return Frequencia.objects.none()
    
    @action(detail=False, methods=['get'])
    def estatisticas(self, request):
        """Retorna estatísticas de frequência por turma"""
        try:
            aluno = request.user.aluno
            turmas = aluno.turmas.filter(ativa=True)
            
            estatisticas = []
            for turma in turmas:
                frequencias = Frequencia.objects.filter(aluno=aluno, aula__turma=turma)
                total = frequencias.count()
                presencas = frequencias.filter(status='PRESENTE').count()
                faltas = frequencias.filter(status='FALTA').count()
                faltas_justificadas = frequencias.filter(status='FALTA_JUSTIFICADA').count()
                
                percentual = (presencas / total * 100) if total > 0 else 0
                
                estatisticas.append({
                    'turma': TurmaSerializer(turma).data,
                    'total_aulas': total,
                    'presencas': presencas,
                    'faltas': faltas,
                    'faltas_justificadas': faltas_justificadas,
                    'percentual_presenca': round(percentual, 1)
                })
            
            return Response(estatisticas)
        except Aluno.DoesNotExist:
            return Response(
                {'erro': 'Usuário não está cadastrado como aluno'},
                status=status.HTTP_404_NOT_FOUND
            )


class AvisoViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet para Avisos (somente leitura)
    """
    queryset = Aviso.objects.filter(ativo=True)
    serializer_class = AvisoSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        if hasattr(user, 'aluno'):
            aluno = user.aluno
            turmas = aluno.turmas.filter(ativa=True)
            return Aviso.objects.filter(
                Q(tipo='GERAL') | 
                Q(turma__in=turmas) | 
                Q(aluno=aluno),
                ativo=True
            ).distinct().order_by('-importante', '-data_criacao')
        return Aviso.objects.none()


class MensalidadeViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet para Mensalidades (somente leitura)
    """
    queryset = Mensalidade.objects.all()
    serializer_class = MensalidadeSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        if hasattr(user, 'aluno'):
            return Mensalidade.objects.filter(aluno=user.aluno).order_by('-mes_referencia')
        return Mensalidade.objects.none()
    
    @action(detail=False, methods=['get'])
    def pendentes(self, request):
        """Retorna mensalidades pendentes"""
        try:
            aluno = request.user.aluno
            mensalidades = Mensalidade.objects.filter(
                aluno=aluno,
                status__in=['PENDENTE', 'ATRASADO']
            ).order_by('data_vencimento')
            
            serializer = self.get_serializer(mensalidades, many=True)
            return Response(serializer.data)
        except Aluno.DoesNotExist:
            return Response(
                {'erro': 'Usuário não está cadastrado como aluno'},
                status=status.HTTP_404_NOT_FOUND
            )


class MensagemViewSet(viewsets.ModelViewSet):
    """
    ViewSet para Mensagens (leitura e escrita)
    """
    queryset = Mensagem.objects.all()
    serializer_class = MensagemSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        # Retorna mensagens recebidas e enviadas pelo usuário
        return Mensagem.objects.filter(
            Q(remetente=user) | Q(destinatario=user)
        ).order_by('-data_envio')
    
    def perform_create(self, serializer):
        # Define o remetente como o usuário logado
        serializer.save(remetente=self.request.user)
    
    @action(detail=False, methods=['get'])
    def recebidas(self, request):
        """Retorna mensagens recebidas"""
        mensagens = Mensagem.objects.filter(
            destinatario=request.user
        ).order_by('-data_envio')
        
        serializer = self.get_serializer(mensagens, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def enviadas(self, request):
        """Retorna mensagens enviadas"""
        mensagens = Mensagem.objects.filter(
            remetente=request.user
        ).order_by('-data_envio')
        
        serializer = self.get_serializer(mensagens, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def marcar_lida(self, request, pk=None):
        """Marca mensagem como lida"""
        mensagem = self.get_object()
        
        if mensagem.destinatario != request.user:
            return Response(
                {'erro': 'Você não tem permissão para marcar esta mensagem como lida'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        mensagem.lida = True
        mensagem.data_leitura = timezone.now()
        mensagem.save()
        
        serializer = self.get_serializer(mensagem)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def nao_lidas(self, request):
        """Retorna contagem de mensagens não lidas"""
        count = Mensagem.objects.filter(
            destinatario=request.user,
            lida=False
        ).count()
        
        return Response({'nao_lidas': count})
