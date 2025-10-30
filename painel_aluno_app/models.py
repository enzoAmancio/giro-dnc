from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.

class Turma(models.Model):
    """Modelo para representar uma turma de dança"""
    MODALIDADES = [
        ('BALLET', 'Ballet'),
        ('JAZZ', 'Jazz'),
        ('HIP_HOP', 'Hip Hop'),
        ('CONTEMPORANEO', 'Contemporâneo'),
        ('DANCA_SALAO', 'Dança de Salão'),
        ('ZUMBA', 'Zumba'),
        ('STREET_DANCE', 'Street Dance'),
    ]
    
    NIVEIS = [
        ('INICIANTE', 'Iniciante'),
        ('INTERMEDIARIO', 'Intermediário'),
        ('AVANCADO', 'Avançado'),
    ]
    
    nome = models.CharField(max_length=100)
    modalidade = models.CharField(max_length=50, choices=MODALIDADES)
    nivel = models.CharField(max_length=20, choices=NIVEIS)
    professor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='turmas_professor')
    capacidade_maxima = models.IntegerField(default=20)
    ativa = models.BooleanField(default=True)
    descricao = models.TextField(blank=True)
    data_inicio = models.DateField(null=True, blank=True)
    data_fim = models.DateField(null=True, blank=True)
    
    class Meta:
        verbose_name = 'Turma'
        verbose_name_plural = 'Turmas'
        ordering = ['nome']
    
    def __str__(self):
        return f"{self.nome} - {self.get_modalidade_display()} ({self.get_nivel_display()})"


class Aluno(models.Model):
    """Modelo para representar um aluno"""
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name='aluno')
    cpf = models.CharField(max_length=14, unique=True)
    data_nascimento = models.DateField()
    telefone = models.CharField(max_length=20)
    telefone_emergencia = models.CharField(max_length=20)
    endereco = models.TextField()
    turmas = models.ManyToManyField(Turma, related_name='alunos', blank=True)
    data_matricula = models.DateField(auto_now_add=True)
    ativo = models.BooleanField(default=True)
    observacoes = models.TextField(blank=True)
    foto = models.ImageField(upload_to='alunos/', blank=True, null=True)
    
    class Meta:
        verbose_name = 'Aluno'
        verbose_name_plural = 'Alunos'
        ordering = ['usuario__first_name', 'usuario__last_name']
    
    def __str__(self):
        return f"{self.usuario.get_full_name()} - {self.cpf}"


class HorarioAula(models.Model):
    """Modelo para representar os horários das aulas"""
    DIAS_SEMANA = [
        ('SEG', 'Segunda-feira'),
        ('TER', 'Terça-feira'),
        ('QUA', 'Quarta-feira'),
        ('QUI', 'Quinta-feira'),
        ('SEX', 'Sexta-feira'),
        ('SAB', 'Sábado'),
        ('DOM', 'Domingo'),
    ]
    
    turma = models.ForeignKey(Turma, on_delete=models.CASCADE, related_name='horarios')
    dia_semana = models.CharField(max_length=3, choices=DIAS_SEMANA)
    hora_inicio = models.TimeField()
    hora_fim = models.TimeField()
    sala = models.CharField(max_length=50, blank=True)
    
    class Meta:
        verbose_name = 'Horário de Aula'
        verbose_name_plural = 'Horários de Aulas'
        ordering = ['dia_semana', 'hora_inicio']
        unique_together = ['turma', 'dia_semana', 'hora_inicio']
    
    def __str__(self):
        return f"{self.turma.nome} - {self.get_dia_semana_display()} {self.hora_inicio.strftime('%H:%M')}"


class Aula(models.Model):
    """Modelo para representar uma aula específica"""
    turma = models.ForeignKey(Turma, on_delete=models.CASCADE, related_name='aulas')
    data = models.DateField()
    hora_inicio = models.TimeField()
    hora_fim = models.TimeField()
    tema = models.CharField(max_length=200, blank=True)
    conteudo = models.TextField(blank=True)
    realizada = models.BooleanField(default=False)
    observacoes = models.TextField(blank=True)
    
    class Meta:
        verbose_name = 'Aula'
        verbose_name_plural = 'Aulas'
        ordering = ['-data', '-hora_inicio']
        unique_together = ['turma', 'data', 'hora_inicio']
    
    def __str__(self):
        return f"{self.turma.nome} - {self.data.strftime('%d/%m/%Y')}"


class Frequencia(models.Model):
    """Modelo para registrar a frequência dos alunos"""
    STATUS_CHOICES = [
        ('PRESENTE', 'Presente'),
        ('FALTA', 'Falta'),
        ('FALTA_JUSTIFICADA', 'Falta Justificada'),
        ('ATESTADO', 'Atestado'),
    ]
    
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE, related_name='frequencias')
    aula = models.ForeignKey(Aula, on_delete=models.CASCADE, related_name='frequencias')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PRESENTE')
    justificativa = models.TextField(blank=True)
    data_registro = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Frequência'
        verbose_name_plural = 'Frequências'
        ordering = ['-aula__data']
        unique_together = ['aluno', 'aula']
    
    def __str__(self):
        return f"{self.aluno.usuario.get_full_name()} - {self.aula} - {self.get_status_display()}"


class Aviso(models.Model):
    """Modelo para avisos e comunicados"""
    TIPO_CHOICES = [
        ('GERAL', 'Geral'),
        ('TURMA', 'Turma Específica'),
        ('ALUNO', 'Aluno Específico'),
        ('EVENTO', 'Evento'),
        ('URGENTE', 'Urgente'),
    ]
    
    titulo = models.CharField(max_length=200)
    conteudo = models.TextField()
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES, default='GERAL')
    autor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='avisos_criados')
    turma = models.ForeignKey(Turma, on_delete=models.CASCADE, null=True, blank=True, related_name='avisos')
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE, null=True, blank=True, related_name='avisos')
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_expiracao = models.DateTimeField(null=True, blank=True)
    ativo = models.BooleanField(default=True)
    importante = models.BooleanField(default=False)
    
    class Meta:
        verbose_name = 'Aviso'
        verbose_name_plural = 'Avisos'
        ordering = ['-importante', '-data_criacao']
    
    def __str__(self):
        return f"{self.titulo} - {self.get_tipo_display()}"


class Mensalidade(models.Model):
    """Modelo para controlar mensalidades dos alunos"""
    STATUS_CHOICES = [
        ('PENDENTE', 'Pendente'),
        ('PAGO', 'Pago'),
        ('ATRASADO', 'Atrasado'),
        ('CANCELADO', 'Cancelado'),
    ]
    
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE, related_name='mensalidades')
    mes_referencia = models.DateField()
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    valor_desconto = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    valor_final = models.DecimalField(max_digits=10, decimal_places=2)
    data_vencimento = models.DateField()
    data_pagamento = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDENTE')
    forma_pagamento = models.CharField(max_length=50, blank=True)
    observacoes = models.TextField(blank=True)
    
    class Meta:
        verbose_name = 'Mensalidade'
        verbose_name_plural = 'Mensalidades'
        ordering = ['-mes_referencia']
        unique_together = ['aluno', 'mes_referencia']
    
    def __str__(self):
        return f"{self.aluno.usuario.get_full_name()} - {self.mes_referencia.strftime('%m/%Y')} - {self.get_status_display()}"
    
    def save(self, *args, **kwargs):
        # Calcula o valor final automaticamente
        self.valor_final = self.valor - self.valor_desconto
        super().save(*args, **kwargs)


class Mensagem(models.Model):
    """Modelo para sistema de mensagens/chat"""
    remetente = models.ForeignKey(User, on_delete=models.CASCADE, related_name='mensagens_enviadas')
    destinatario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='mensagens_recebidas')
    assunto = models.CharField(max_length=200, blank=True)
    conteudo = models.TextField()
    data_envio = models.DateTimeField(auto_now_add=True)
    lida = models.BooleanField(default=False)
    data_leitura = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        verbose_name = 'Mensagem'
        verbose_name_plural = 'Mensagens'
        ordering = ['-data_envio']
    
    def __str__(self):
        return f"De {self.remetente.username} para {self.destinatario.username} - {self.data_envio.strftime('%d/%m/%Y %H:%M')}"
 