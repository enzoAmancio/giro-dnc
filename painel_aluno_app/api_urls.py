from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .viewsets import (
    AlunoViewSet, TurmaViewSet, AulaViewSet, HorarioAulaViewSet,
    FrequenciaViewSet, AvisoViewSet, MensalidadeViewSet, MensagemViewSet
)

router = DefaultRouter()
router.register(r'alunos', AlunoViewSet, basename='aluno')
router.register(r'turmas', TurmaViewSet, basename='turma')
router.register(r'aulas', AulaViewSet, basename='aula')
router.register(r'horarios', HorarioAulaViewSet, basename='horario')
router.register(r'frequencias', FrequenciaViewSet, basename='frequencia')
router.register(r'avisos', AvisoViewSet, basename='aviso')
router.register(r'mensalidades', MensalidadeViewSet, basename='mensalidade')
router.register(r'mensagens', MensagemViewSet, basename='mensagem')

urlpatterns = [
    path('', include(router.urls)),
]
