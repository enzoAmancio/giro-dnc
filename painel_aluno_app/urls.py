from django.urls import path
from . import views

urlpatterns = [
    path('', views.painel_aluno, name='painel_aluno'),
    
]
