from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator, FileExtensionValidator
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.db.models import Sum
import os

# Create your models here.

def validate_video_size(value):
    """Valida o tamanho do arquivo de vídeo (máximo 50MB)"""
    filesize = value.size
    max_size_mb = 50
    max_size_bytes = max_size_mb * 1024 * 1024  # 50MB em bytes
    
    if filesize > max_size_bytes:
        raise ValidationError(f'O tamanho máximo do arquivo é {max_size_mb}MB. Seu arquivo tem {filesize / 1024 / 1024:.2f}MB.')
    return value

def video_upload_path(instance, filename):
    """Define o caminho de upload dos vídeos organizados por turma e data"""
    # Remove caracteres especiais do nome da turma
    turma_nome = instance.turma.nome.replace(' ', '_').replace('/', '-')
    data_str = instance.data.strftime('%Y-%m-%d')
    
    # Mantém a extensão original do arquivo
    ext = filename.split('.')[-1]
    filename_safe = f"{data_str}_{instance.tema[:30] if instance.tema else 'aula'}.{ext}"
    
    return f'aulas/videos/{turma_nome}/{filename_safe}'

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
    capacidade_maxima = models.IntegerField(default=20, validators=[MinValueValidator(1)])
    ativa = models.BooleanField(default=True)
    descricao = models.TextField(blank=True)
    data_inicio = models.DateField(null=True, blank=True)
    data_fim = models.DateField(null=True, blank=True)
    
    class Meta:
        verbose_name = 'Turma'
        verbose_name_plural = 'Turmas'
        ordering = ['nome']
    
    def clean(self):
        """Validação customizada"""
        super().clean()
        if self.data_inicio and self.data_fim:
            if self.data_fim < self.data_inicio:
                raise ValidationError({
                    'data_fim': 'Data de término não pode ser anterior à data de início.'
                })
    
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
    
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
    
    def clean(self):
        """Validação customizada"""
        super().clean()
        if self.hora_inicio and self.hora_fim:
            if self.hora_fim <= self.hora_inicio:
                raise ValidationError({
                    'hora_fim': 'Horário de término deve ser posterior ao horário de início.'
                })
    
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
    
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
    video = models.FileField(
        upload_to=video_upload_path,
        blank=True,
        null=True,
        validators=[
            validate_video_size,
            FileExtensionValidator(allowed_extensions=['mp4', 'webm', 'avi', 'mov'])
        ],
        help_text='Vídeo da aula (máximo 50MB). Formatos: MP4, WebM, AVI, MOV'
    )
    data_upload_video = models.DateTimeField(blank=True, null=True, help_text='Data do upload do vídeo')
    
    class Meta:
        verbose_name = 'Aula'
        verbose_name_plural = 'Aulas'
        ordering = ['-data', '-hora_inicio']
        unique_together = ['turma', 'data', 'hora_inicio']
    
    def __str__(self):
        return f"{self.turma.nome} - {self.data.strftime('%d/%m/%Y')}"
    
    def save(self, *args, **kwargs):
        # Atualiza a data de upload do vídeo se um novo vídeo foi adicionado
        if self.video and not self.data_upload_video:
            self.data_upload_video = timezone.now()
        super().save(*args, **kwargs)
    
    def delete(self, *args, **kwargs):
        # Deleta o arquivo de vídeo do storage quando a aula for deletada
        if self.video:
            if os.path.isfile(self.video.path):
                os.remove(self.video.path)
        super().delete(*args, **kwargs)
    
    def get_video_size_mb(self):
        """Retorna o tamanho do vídeo em MB"""
        if self.video:
            return self.video.size / 1024 / 1024
        return 0
    
    def dias_desde_upload(self):
        """Retorna quantos dias se passaram desde o upload do vídeo"""
        if self.data_upload_video:
            return (timezone.now() - self.data_upload_video).days
        return None


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
    valor = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    valor_desconto = models.DecimalField(max_digits=10, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    valor_final = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
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
    
    def clean(self):
        """Validação customizada"""
        super().clean()
        if self.valor_desconto and self.valor:
            if self.valor_desconto > self.valor:
                raise ValidationError({
                    'valor_desconto': 'Desconto não pode ser maior que o valor da mensalidade.'
                })
        if self.data_pagamento and self.status != 'PAGO':
            raise ValidationError({
                'status': 'Status deve ser "PAGO" quando há data de pagamento.'
            })
    
    def save(self, *args, **kwargs):
        # Calcula o valor final automaticamente
        if self.valor is not None and self.valor_desconto is not None:
            self.valor_final = self.valor - self.valor_desconto
        
        # Atualiza status para ATRASADO se vencida
        if self.status == 'PENDENTE' and self.data_vencimento < timezone.now().date():
            self.status = 'ATRASADO'
        
        self.full_clean()
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.aluno.usuario.get_full_name()} - {self.mes_referencia.strftime('%m/%Y')} - {self.get_status_display()}"
    
    def esta_atrasada(self):
        """Verifica se a mensalidade está atrasada"""
        return self.status in ['PENDENTE', 'ATRASADO'] and self.data_vencimento < timezone.now().date()
    
    def dias_em_atraso(self):
        """Retorna quantos dias está em atraso"""
        if self.esta_atrasada():
            return (timezone.now().date() - self.data_vencimento).days
        return 0


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


class Notificacao(models.Model):
    """Modelo para notificações do sistema"""
    TIPO_CHOICES = [
        ('INFO', 'Informação'),
        ('AVISO', 'Aviso'),
        ('SUCESSO', 'Sucesso'),
        ('ALERTA', 'Alerta'),
        ('ERRO', 'Erro'),
    ]
    
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notificacoes')
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES, default='INFO')
    titulo = models.CharField(max_length=200)
    mensagem = models.TextField()
    link = models.CharField(max_length=500, blank=True, help_text='URL para onde a notificação deve levar')
    lida = models.BooleanField(default=False)
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_leitura = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        verbose_name = 'Notificação'
        verbose_name_plural = 'Notificações'
        ordering = ['-data_criacao']
    
    def __str__(self):
        return f"{self.tipo} - {self.titulo} para {self.usuario.username}"
    
    def marcar_como_lida(self):
        """Marca a notificação como lida"""
        if not self.lida:
            self.lida = True
            self.data_leitura = timezone.now()
            self.save()


class Evento(models.Model):
    """Modelo para eventos com venda de ingressos"""
    nome = models.CharField(max_length=200, help_text='Nome do evento (ex: Corpo e Som)')
    descricao = models.TextField(blank=True, help_text='Descrição do evento')
    data_evento = models.DateField(help_text='Data de realização do evento')
    hora_evento = models.TimeField(blank=True, null=True, help_text='Horário do evento')
    local = models.CharField(max_length=200, blank=True, help_text='Local do evento')
    valor_ingresso = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        validators=[MinValueValidator(0)],
        help_text='Valor do ingresso'
    )
    meta_vendas = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0)],
        help_text='Meta de ingressos a serem vendidos'
    )
    comissao_percentual = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        help_text='Percentual de comissão por ingresso vendido (0-100%)'
    )
    ativo = models.BooleanField(default=True, help_text='Evento ativo para vendas')
    data_criacao = models.DateTimeField(auto_now_add=True)
    criado_por = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        related_name='eventos_criados'
    )
    imagem = models.ImageField(
        upload_to='eventos/',
        blank=True,
        null=True,
        help_text='Imagem/banner do evento'
    )
    
    class Meta:
        verbose_name = 'Evento'
        verbose_name_plural = 'Eventos'
        ordering = ['-data_evento', '-data_criacao']
    
    def __str__(self):
        return f"{self.nome} - {self.data_evento.strftime('%d/%m/%Y')}"
    
    def total_vendido(self):
        """Retorna o total de ingressos vendidos"""
        return self.vendas.aggregate(total=Sum('quantidade'))['total'] or 0
    
    def total_arrecadado(self):
        """Retorna o valor total arrecadado"""
        return self.total_vendido() * self.valor_ingresso
    
    def percentual_meta(self):
        """Retorna o percentual da meta atingido"""
        if self.meta_vendas > 0:
            return (self.total_vendido() / self.meta_vendas) * 100
        return 0
    
    def ingressos_restantes(self):
        """Retorna quantos ingressos faltam para atingir a meta"""
        restante = self.meta_vendas - self.total_vendido()
        return max(0, restante)


class VendaIngresso(models.Model):
    """Modelo para registrar vendas de ingressos pelos dançarinos"""
    evento = models.ForeignKey(Evento, on_delete=models.CASCADE, related_name='vendas')
    vendedor = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='vendas_ingressos',
        help_text='Dançarino que realizou a venda'
    )
    quantidade = models.IntegerField(
        validators=[MinValueValidator(1)],
        help_text='Quantidade de ingressos vendidos'
    )
    data_venda = models.DateField(default=timezone.now, help_text='Data da venda')
    data_registro = models.DateTimeField(auto_now_add=True, help_text='Data/hora do registro')
    observacoes = models.TextField(blank=True, help_text='Observações sobre a venda')
    confirmado = models.BooleanField(
        default=False,
        help_text='Venda confirmada pela administração'
    )
    valor_comissao = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(0)],
        help_text='Valor da comissão do vendedor'
    )
    
    class Meta:
        verbose_name = 'Venda de Ingresso'
        verbose_name_plural = 'Vendas de Ingressos'
        ordering = ['-data_venda', '-data_registro']
    
    def __str__(self):
        return f"{self.vendedor.get_full_name() or self.vendedor.username} - {self.evento.nome} ({self.quantidade} ingressos)"
    
    def save(self, *args, **kwargs):
        # Calcula a comissão automaticamente
        if self.evento.comissao_percentual > 0:
            valor_total = self.quantidade * self.evento.valor_ingresso
            self.valor_comissao = (valor_total * self.evento.comissao_percentual) / 100
        super().save(*args, **kwargs)
    
    def valor_total(self):
        """Retorna o valor total da venda"""
        return self.quantidade * self.evento.valor_ingresso


class ResultadoFinanceiroMensal(models.Model):
    """
    Model para armazenar resultados financeiros mensais da Giro DNC.
    Permite ao administrador visualizar lucros, gastos e valores a receber mês a mês.
    """
    # Mês de referência (ex: "2025-01" para Janeiro/2025)
    mes = models.DateField(
        verbose_name="Mês de Referência",
        help_text="Selecione o primeiro dia do mês de referência",
        unique=True  # Garante um único registro por mês
    )
    
    # Valores financeiros
    lucro_total = models.DecimalField(
        verbose_name="Lucro Total",
        max_digits=10,
        decimal_places=2,
        default=0.00,
        validators=[MinValueValidator(0)],
        help_text="Total de receitas/lucros no mês"
    )
    
    gasto_total = models.DecimalField(
        verbose_name="Gasto Total",
        max_digits=10,
        decimal_places=2,
        default=0.00,
        validators=[MinValueValidator(0)],
        help_text="Total de despesas/gastos no mês"
    )
    
    a_receber_total = models.DecimalField(
        verbose_name="A Receber Total",
        max_digits=10,
        decimal_places=2,
        default=0.00,
        validators=[MinValueValidator(0)],
        help_text="Total de valores pendentes a receber"
    )
    
    # Metadados
    observacoes = models.TextField(
        verbose_name="Observações",
        blank=True,
        null=True,
        help_text="Anotações ou detalhes adicionais sobre o mês"
    )
    
    data_criacao = models.DateTimeField(
        verbose_name="Data de Criação",
        auto_now_add=True
    )
    
    data_atualizacao = models.DateTimeField(
        verbose_name="Última Atualização",
        auto_now=True
    )
    
    criado_por = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Criado por",
        related_name='resultados_financeiros_criados'
    )
    
    class Meta:
        verbose_name = "Resultado Financeiro Mensal"
        verbose_name_plural = "Resultados Financeiros Mensais"
        ordering = ['-mes']  # Mais recentes primeiro
        indexes = [
            models.Index(fields=['-mes']),
        ]
    
    def __str__(self):
        return f"{self.mes.strftime('%B/%Y')} - Lucro Líquido: R$ {self.lucro_liquido():.2f}"
    
    def lucro_liquido(self):
        """
        Calcula o lucro líquido: Lucro Total - Gasto Total
        Returns:
            Decimal: Valor do lucro líquido (pode ser negativo se gastos > lucros)
        """
        return self.lucro_total - self.gasto_total
    
    def percentual_gastos(self):
        """
        Calcula o percentual de gastos em relação ao lucro total
        Returns:
            float: Percentual de gastos (0-100)
        """
        if self.lucro_total > 0:
            return float((self.gasto_total / self.lucro_total) * 100)
        return 0.0
    
    def percentual_a_receber(self):
        """
        Calcula o percentual de valores a receber em relação ao lucro total
        Returns:
            float: Percentual a receber (0-100)
        """
        if self.lucro_total > 0:
            return float((self.a_receber_total / self.lucro_total) * 100)
        return 0.0
    
    def mes_formatado(self):
        """
        Retorna o mês formatado em português
        Returns:
            str: Mês/Ano (ex: "Janeiro/2025")
        """
        meses_pt = {
            1: 'Janeiro', 2: 'Fevereiro', 3: 'Março', 4: 'Abril',
            5: 'Maio', 6: 'Junho', 7: 'Julho', 8: 'Agosto',
            9: 'Setembro', 10: 'Outubro', 11: 'Novembro', 12: 'Dezembro'
        }
        return f"{meses_pt[self.mes.month]}/{self.mes.year}"
    
    def dados_grafico(self):
        """
        Retorna os dados formatados para o gráfico doughnut
        Returns:
            dict: Dicionário com labels e valores para Chart.js
        """
        return {
            'labels': ['Lucro Líquido', 'Gastos', 'A Receber'],
            'valores': [
                float(self.lucro_liquido()),
                float(self.gasto_total),
                float(self.a_receber_total)
            ],
            'cores': ['#22c55e', '#ef4444', '#f97316']  # Verde, Vermelho, Laranja
        }


class DespesaAluno(models.Model):
    """
    Model para alunos registrarem suas próprias despesas relacionadas às atividades.
    Exemplos: viagens, figurinos, acessórios, transporte, alimentação em eventos, etc.
    Cada aluno gerencia suas próprias despesas.
    """
    CATEGORIA_CHOICES = [
        ('FIGURINO', 'Figurino'),
        ('VIAGEM', 'Viagem/Excursão'),
        ('APRESENTACAO', 'Apresentação/Evento'),
        ('ACESSORIO', 'Acessórios'),
        ('TRANSPORTE', 'Transporte'),
        ('ALIMENTACAO', 'Alimentação'),
        ('HOSPEDAGEM', 'Hospedagem'),
        ('MAQUIAGEM', 'Maquiagem/Caracterização'),
        ('CABELO', 'Cabelo/Penteado'),
        ('SAPATO', 'Sapatos/Calçados'),
        ('OUTRO', 'Outro'),
    ]
    
    STATUS_CHOICES = [
        ('PLANEJADO', 'Planejado'),
        ('PAGO', 'Pago'),
        ('PARCIAL', 'Parcialmente Pago'),
        ('CANCELADO', 'Cancelado'),
    ]
    
    # Relação com aluno
    aluno = models.ForeignKey(
        Aluno,
        on_delete=models.CASCADE,
        verbose_name="Aluno",
        related_name='despesas_pessoais',
        help_text="Aluno que registrou esta despesa"
    )
    
    # Informações da despesa
    nome = models.CharField(
        verbose_name="Nome da Despesa",
        max_length=200,
        help_text="Ex: Viagem para São Paulo - Agosto/2025"
    )
    
    descricao = models.CharField(
        verbose_name="Descrição",
        max_length=300,
        help_text="Breve descrição (ex: Figurino completo para apresentação de Natal)"
    )
    
    categoria = models.CharField(
        verbose_name="Categoria",
        max_length=20,
        choices=CATEGORIA_CHOICES,
        default='OUTRO'
    )
    
    # Relação opcional com turma (para contextualizar)
    turma = models.ForeignKey(
        Turma,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Turma Relacionada",
        help_text="Turma ou evento relacionado (opcional)"
    )
    
    # Valores
    valor_previsto = models.DecimalField(
        verbose_name="Valor Previsto",
        max_digits=10,
        decimal_places=2,
        default=0.00,
        validators=[MinValueValidator(0)],
        help_text="Quanto você estima gastar"
    )
    
    valor_gasto = models.DecimalField(
        verbose_name="Valor Gasto",
        max_digits=10,
        decimal_places=2,
        default=0.00,
        validators=[MinValueValidator(0)],
        help_text="Quanto você já gastou"
    )
    
    status = models.CharField(
        verbose_name="Status",
        max_length=20,
        choices=STATUS_CHOICES,
        default='PLANEJADO'
    )
    
    # Datas
    data_prevista = models.DateField(
        verbose_name="Data Prevista",
        help_text="Quando você prevê esta despesa (ex: data da viagem)"
    )
    
    data_pagamento = models.DateField(
        verbose_name="Data do Pagamento",
        null=True,
        blank=True,
        help_text="Quando você pagou ou vai pagar"
    )
    
    # Detalhes adicionais
    observacoes = models.TextField(
        verbose_name="Observações",
        blank=True,
        null=True,
        help_text="Anotações adicionais, lembretes, detalhes de parcelamento, etc."
    )
    
    # Controle de itens (opcional - para detalhar o que compõe a despesa)
    itens = models.TextField(
        verbose_name="Itens",
        blank=True,
        null=True,
        help_text="Lista de itens que compõem esta despesa (ex: vestido, sapato, maquiagem)"
    )
    
    # Metadados
    data_criacao = models.DateTimeField(
        verbose_name="Data de Criação",
        auto_now_add=True
    )
    
    data_atualizacao = models.DateTimeField(
        verbose_name="Última Atualização",
        auto_now=True
    )
    
    class Meta:
        verbose_name = "Despesa do Aluno"
        verbose_name_plural = "Despesas dos Alunos"
        ordering = ['-data_prevista', '-data_criacao']
        indexes = [
            models.Index(fields=['aluno', '-data_prevista']),
            models.Index(fields=['status']),
            models.Index(fields=['categoria']),
        ]
    
    def __str__(self):
        return f"{self.aluno.usuario.get_full_name()} - {self.nome}"
    
    def valor_restante(self):
        """Calcula quanto ainda falta gastar em relação ao previsto"""
        return self.valor_previsto - self.valor_gasto
    
    def percentual_gasto(self):
        """Calcula o percentual já gasto em relação ao previsto"""
        if self.valor_previsto > 0:
            return float((self.valor_gasto / self.valor_previsto) * 100)
        return 0.0
    
    def esta_dentro_orcamento(self):
        """Verifica se está dentro do orçamento previsto"""
        return self.valor_gasto <= self.valor_previsto
    
    def diferenca_orcamento(self):
        """Retorna a diferença (positiva = economia, negativa = estouro)"""
        return self.valor_previsto - self.valor_gasto
    
    def categoria_display(self):
        """Retorna o nome da categoria formatado"""
        return dict(self.CATEGORIA_CHOICES).get(self.categoria, self.categoria)
    
    def status_display(self):
        """Retorna o nome do status formatado"""
        return dict(self.STATUS_CHOICES).get(self.status, self.status)
    
    def mes_formatado(self):
        """Retorna o mês/ano da despesa prevista"""
        meses_pt = {
            1: 'Janeiro', 2: 'Fevereiro', 3: 'Março', 4: 'Abril',
            5: 'Maio', 6: 'Junho', 7: 'Julho', 8: 'Agosto',
            9: 'Setembro', 10: 'Outubro', 11: 'Novembro', 12: 'Dezembro'
        }
        return f"{meses_pt[self.data_prevista.month]}/{self.data_prevista.year}"
    
    def status_cor(self):
        """Retorna a cor apropriada para o status"""
        cores = {
            'PLANEJADO': '#f97316',  # Laranja
            'PAGO': '#22c55e',       # Verde
            'PARCIAL': '#eab308',    # Amarelo
            'CANCELADO': '#6b7280',  # Cinza
        }
        return cores.get(self.status, '#6b7280')
    
    def get_categoria_color(self):
        """Retorna a cor apropriada para cada categoria"""
        cores = {
            'FIGURINO': '#3b82f6',      # Azul
            'VIAGEM': '#ef4444',        # Vermelho
            'APRESENTACAO': '#22c55e',  # Verde
            'ACESSORIO': '#f59e0b',     # Âmbar
            'TRANSPORTE': '#8b5cf6',    # Roxo
            'ALIMENTACAO': '#ec4899',   # Pink
            'HOSPEDAGEM': '#14b8a6',    # Teal
            'MAQUIAGEM': '#f97316',     # Laranja
            'CABELO': '#6366f1',        # Indigo
            'SAPATO': '#84cc16',        # Lima
            'OUTRO': '#6b7280',         # Cinza
        }
        return cores.get(self.categoria, '#6b7280')
    
    def get_status_color(self):
        """Retorna a cor apropriada para o status (mesmo que status_cor)"""
        return self.status_cor()


class DespesaAdministrativa(models.Model):
    """
    Model para gerenciar despesas administrativas da Giro DNC
    (Aluguel, contas, salários, equipamentos, manutenção, etc.)
    """
    
    CATEGORIA_CHOICES = [
        ('ALUGUEL', 'Aluguel'),
        ('ENERGIA', 'Energia Elétrica'),
        ('AGUA', 'Água'),
        ('INTERNET', 'Internet/Telefone'),
        ('SALARIO', 'Salários'),
        ('EQUIPAMENTO', 'Equipamentos'),
        ('MANUTENCAO', 'Manutenção'),
        ('LIMPEZA', 'Limpeza'),
        ('MATERIAL', 'Material de Consumo'),
        ('MARKETING', 'Marketing/Publicidade'),
        ('IMPOSTOS', 'Impostos/Taxas'),
        ('SEGURO', 'Seguros'),
        ('TRANSPORTE', 'Transporte/Combustível'),
        ('ALIMENTACAO', 'Alimentação'),
        ('EVENTO', 'Eventos/Apresentações'),
        ('SOFTWARE', 'Software/Licenças'),
        ('JURIDICO', 'Jurídico/Contábil'),
        ('OUTRO', 'Outros'),
    ]
    
    STATUS_CHOICES = [
        ('PENDENTE', 'Pendente'),
        ('PAGO', 'Pago'),
        ('ATRASADO', 'Atrasado'),
        ('PARCIAL', 'Parcialmente Pago'),
        ('CANCELADO', 'Cancelado'),
    ]
    
    TIPO_PAGAMENTO_CHOICES = [
        ('FIXO', 'Fixo (Mensal)'),
        ('VARIAVEL', 'Variável'),
        ('UNICO', 'Único'),
        ('PARCELADO', 'Parcelado'),
    ]
    
    FORMA_PAGAMENTO_CHOICES = [
        ('DINHEIRO', 'Dinheiro'),
        ('DEBITO', 'Cartão de Débito'),
        ('CREDITO', 'Cartão de Crédito'),
        ('PIX', 'PIX'),
        ('TRANSFERENCIA', 'Transferência Bancária'),
        ('BOLETO', 'Boleto'),
        ('CHEQUE', 'Cheque'),
    ]
    
    # Informações Básicas
    nome = models.CharField(
        verbose_name="Nome da Despesa",
        max_length=200,
        help_text="Ex: Aluguel Janeiro 2025, Conta de Luz, Salário Professor João",
        default="Nova Despesa"
    )
    
    categoria = models.CharField(
        verbose_name="Categoria",
        max_length=20,
        choices=CATEGORIA_CHOICES,
        default='OUTRO'
    )
    
    descricao = models.TextField(
        verbose_name="Descrição",
        blank=True,
        null=True,
        help_text="Detalhes sobre a despesa"
    )
    
    # Fornecedor/Beneficiário
    fornecedor = models.CharField(
        verbose_name="Fornecedor/Beneficiário",
        max_length=200,
        blank=True,
        null=True,
        help_text="Nome da empresa ou pessoa que receberá o pagamento"
    )
    
    # Valores
    valor_total = models.DecimalField(
        verbose_name="Valor Total",
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        help_text="Valor total da despesa",
        default=0.00
    )
    
    valor_pago = models.DecimalField(
        verbose_name="Valor Pago",
        max_digits=10,
        decimal_places=2,
        default=0.00,
        validators=[MinValueValidator(0)],
        help_text="Quanto já foi pago"
    )
    
    # Datas
    data_vencimento = models.DateField(
        verbose_name="Data de Vencimento",
        help_text="Data limite para pagamento",
        null=True,
        blank=True
    )
    
    data_pagamento = models.DateField(
        verbose_name="Data do Pagamento",
        null=True,
        blank=True,
        help_text="Quando foi efetivamente pago"
    )
    
    # Status e Tipo
    status = models.CharField(
        verbose_name="Status",
        max_length=20,
        choices=STATUS_CHOICES,
        default='PENDENTE'
    )
    
    tipo_pagamento = models.CharField(
        verbose_name="Tipo de Pagamento",
        max_length=20,
        choices=TIPO_PAGAMENTO_CHOICES,
        default='UNICO'
    )
    
    forma_pagamento = models.CharField(
        verbose_name="Forma de Pagamento",
        max_length=20,
        choices=FORMA_PAGAMENTO_CHOICES,
        blank=True,
        null=True
    )
    
    # Parcelamento (se aplicável)
    numero_parcelas = models.IntegerField(
        verbose_name="Número de Parcelas",
        null=True,
        blank=True,
        validators=[MinValueValidator(1)],
        help_text="Se for parcelado, quantas parcelas?"
    )
    
    parcela_atual = models.IntegerField(
        verbose_name="Parcela Atual",
        null=True,
        blank=True,
        validators=[MinValueValidator(1)],
        help_text="Qual parcela é esta?"
    )
    
    # Documentação
    numero_documento = models.CharField(
        verbose_name="Nº do Documento",
        max_length=100,
        blank=True,
        null=True,
        help_text="Número da nota fiscal, boleto, recibo, etc."
    )
    
    comprovante = models.FileField(
        verbose_name="Comprovante",
        upload_to='despesas_admin/comprovantes/',
        blank=True,
        null=True,
        help_text="Upload do comprovante de pagamento"
    )
    
    # Observações
    observacoes = models.TextField(
        verbose_name="Observações",
        blank=True,
        null=True,
        help_text="Anotações adicionais, lembretes, condições especiais"
    )
    
    # Metadados
    criado_por = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='despesas_criadas',
        verbose_name="Criado por"
    )
    
    data_criacao = models.DateTimeField(
        verbose_name="Data de Criação",
        auto_now_add=True
    )
    
    data_atualizacao = models.DateTimeField(
        verbose_name="Última Atualização",
        auto_now=True
    )
    
    class Meta:
        verbose_name = "Despesa Administrativa"
        verbose_name_plural = "Despesas Administrativas"
        ordering = ['-data_vencimento', '-data_criacao']
        indexes = [
            models.Index(fields=['-data_vencimento']),
            models.Index(fields=['status']),
            models.Index(fields=['categoria']),
            models.Index(fields=['tipo_pagamento']),
        ]
    
    def __str__(self):
        return f"{self.nome} - R$ {self.valor_total}"
    
    def valor_pendente(self):
        """Calcula quanto ainda falta pagar"""
        return self.valor_total - self.valor_pago
    
    def percentual_pago(self):
        """Calcula o percentual já pago"""
        if self.valor_total > 0:
            return float((self.valor_pago / self.valor_total) * 100)
        return 0.0
    
    def esta_pago(self):
        """Verifica se está totalmente pago"""
        return self.valor_pago >= self.valor_total
    
    def esta_atrasado(self):
        """Verifica se está atrasado"""
        if self.status == 'PAGO':
            return False
        from datetime import date
        return self.data_vencimento < date.today()
    
    def dias_ate_vencimento(self):
        """Calcula quantos dias faltam para o vencimento"""
        from datetime import date
        delta = self.data_vencimento - date.today()
        return delta.days
    
    def categoria_display(self):
        """Retorna o nome da categoria formatado"""
        return dict(self.CATEGORIA_CHOICES).get(self.categoria, self.categoria)
    
    def status_display(self):
        """Retorna o nome do status formatado"""
        return dict(self.STATUS_CHOICES).get(self.status, self.status)
    
    def mes_formatado(self):
        """Retorna o mês/ano do vencimento"""
        meses_pt = {
            1: 'Janeiro', 2: 'Fevereiro', 3: 'Março', 4: 'Abril',
            5: 'Maio', 6: 'Junho', 7: 'Julho', 8: 'Agosto',
            9: 'Setembro', 10: 'Outubro', 11: 'Novembro', 12: 'Dezembro'
        }
        return f"{meses_pt[self.data_vencimento.month]}/{self.data_vencimento.year}"
    
    def get_categoria_color(self):
        """Retorna a cor apropriada para cada categoria"""
        cores = {
            'ALUGUEL': '#ef4444',        # Vermelho
            'ENERGIA': '#f59e0b',        # Âmbar
            'AGUA': '#3b82f6',           # Azul
            'INTERNET': '#8b5cf6',       # Roxo
            'SALARIO': '#22c55e',        # Verde
            'EQUIPAMENTO': '#06b6d4',    # Ciano
            'MANUTENCAO': '#f97316',     # Laranja
            'LIMPEZA': '#14b8a6',        # Teal
            'MATERIAL': '#6366f1',       # Indigo
            'MARKETING': '#ec4899',      # Pink
            'IMPOSTOS': '#dc2626',       # Vermelho Escuro
            'SEGURO': '#0ea5e9',         # Azul Céu
            'TRANSPORTE': '#a855f7',     # Roxo
            'ALIMENTACAO': '#84cc16',    # Lima
            'EVENTO': '#f43f5e',         # Rosa
            'SOFTWARE': '#6366f1',       # Indigo
            'JURIDICO': '#334155',       # Ardósia
            'OUTRO': '#6b7280',          # Cinza
        }
        return cores.get(self.categoria, '#6b7280')
    
    def get_status_color(self):
        """Retorna a cor apropriada para o status"""
        cores = {
            'PENDENTE': '#f59e0b',    # Âmbar
            'PAGO': '#22c55e',        # Verde
            'ATRASADO': '#ef4444',    # Vermelho
            'PARCIAL': '#3b82f6',     # Azul
            'CANCELADO': '#6b7280',   # Cinza
        }
        return cores.get(self.status, '#6b7280')
    
    def get_status_badge_class(self):
        """Retorna a classe Bootstrap para o badge de status"""
        classes = {
            'PENDENTE': 'bg-warning',
            'PAGO': 'bg-success',
            'ATRASADO': 'bg-danger',
            'PARCIAL': 'bg-info',
            'CANCELADO': 'bg-secondary',
        }
        return classes.get(self.status, 'bg-secondary')
    
    def parcelas_display(self):
        """Retorna string formatada das parcelas"""
        if self.numero_parcelas and self.parcela_atual:
            return f"{self.parcela_atual}/{self.numero_parcelas}"
        return "-"


class EntradaFinanceira(models.Model):
    """
    Model para registrar entradas/receitas administrativas da Giro DNC
    (Mensalidades, vendas de ingressos, patrocínios, etc.)
    """
    
    CATEGORIA_CHOICES = [
        ('MENSALIDADE', 'Mensalidades'),
        ('INGRESSO', 'Venda de Ingressos'),
        ('PATROCINIO', 'Patrocínio'),
        ('DOACAO', 'Doação'),
        ('WORKSHOP', 'Workshop/Curso'),
        ('ALUGUEL_ESPACO', 'Aluguel de Espaço'),
        ('APRESENTACAO', 'Apresentação/Show'),
        ('MERCHANDISING', 'Venda de Produtos'),
        ('CONSULTA', 'Consultoria'),
        ('OUTRO', 'Outros'),
    ]
    
    STATUS_CHOICES = [
        ('PENDENTE', 'Pendente'),
        ('RECEBIDO', 'Recebido'),
        ('ATRASADO', 'Atrasado'),
        ('PARCIAL', 'Parcialmente Recebido'),
        ('CANCELADO', 'Cancelado'),
    ]
    
    FORMA_RECEBIMENTO_CHOICES = [
        ('DINHEIRO', 'Dinheiro'),
        ('DEBITO', 'Cartão de Débito'),
        ('CREDITO', 'Cartão de Crédito'),
        ('PIX', 'PIX'),
        ('TRANSFERENCIA', 'Transferência Bancária'),
        ('BOLETO', 'Boleto'),
        ('CHEQUE', 'Cheque'),
    ]
    
    # Informações Básicas
    nome = models.CharField(
        verbose_name="Nome da Entrada",
        max_length=200,
        help_text="Ex: Mensalidade João Silva - Janeiro 2025",
        default="Nova Entrada"
    )
    
    categoria = models.CharField(
        verbose_name="Categoria",
        max_length=20,
        choices=CATEGORIA_CHOICES,
        default='OUTRO'
    )
    
    descricao = models.TextField(
        verbose_name="Descrição",
        blank=True,
        null=True,
        help_text="Detalhes sobre a entrada"
    )
    
    # Pagador/Origem
    pagador = models.CharField(
        verbose_name="Pagador/Origem",
        max_length=200,
        blank=True,
        null=True,
        help_text="Nome da pessoa ou empresa que pagou"
    )
    
    # Valores
    valor_total = models.DecimalField(
        verbose_name="Valor Total",
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        help_text="Valor total esperado",
        default=0.00
    )
    
    valor_recebido = models.DecimalField(
        verbose_name="Valor Recebido",
        max_digits=10,
        decimal_places=2,
        default=0.00,
        validators=[MinValueValidator(0)],
        help_text="Quanto já foi recebido"
    )
    
    # Datas
    data_prevista = models.DateField(
        verbose_name="Data Prevista",
        help_text="Data esperada do recebimento",
        null=True,
        blank=True
    )
    
    data_recebimento = models.DateField(
        verbose_name="Data do Recebimento",
        null=True,
        blank=True,
        help_text="Quando foi efetivamente recebido"
    )
    
    # Status e Forma
    status = models.CharField(
        verbose_name="Status",
        max_length=20,
        choices=STATUS_CHOICES,
        default='PENDENTE'
    )
    
    forma_recebimento = models.CharField(
        verbose_name="Forma de Recebimento",
        max_length=20,
        choices=FORMA_RECEBIMENTO_CHOICES,
        blank=True,
        null=True
    )
    
    # Parcelamento
    numero_parcelas = models.IntegerField(
        verbose_name="Número de Parcelas",
        null=True,
        blank=True,
        validators=[MinValueValidator(1)],
        help_text="Se for parcelado, quantas parcelas?"
    )
    
    parcela_atual = models.IntegerField(
        verbose_name="Parcela Atual",
        null=True,
        blank=True,
        validators=[MinValueValidator(1)],
        help_text="Qual parcela é esta?"
    )
    
    # Documentação
    numero_documento = models.CharField(
        verbose_name="Nº do Documento",
        max_length=100,
        blank=True,
        null=True,
        help_text="Número do recibo, nota fiscal, etc."
    )
    
    comprovante = models.FileField(
        verbose_name="Comprovante",
        upload_to='entradas_admin/comprovantes/',
        blank=True,
        null=True,
        help_text="Upload do comprovante de recebimento"
    )
    
    # Observações
    observacoes = models.TextField(
        verbose_name="Observações",
        blank=True,
        null=True,
        help_text="Anotações adicionais"
    )
    
    # Metadados
    criado_por = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='entradas_criadas',
        verbose_name="Criado por"
    )
    
    data_criacao = models.DateTimeField(
        verbose_name="Data de Criação",
        auto_now_add=True
    )
    
    data_atualizacao = models.DateTimeField(
        verbose_name="Última Atualização",
        auto_now=True
    )
    
    class Meta:
        verbose_name = "Entrada Financeira"
        verbose_name_plural = "Entradas Financeiras"
        ordering = ['-data_prevista', '-data_criacao']
        indexes = [
            models.Index(fields=['-data_prevista']),
            models.Index(fields=['status']),
            models.Index(fields=['categoria']),
        ]
    
    def __str__(self):
        return f"{self.nome} - R$ {self.valor_total}"
    
    def valor_pendente(self):
        """Calcula quanto ainda falta receber"""
        return self.valor_total - self.valor_recebido
    
    def percentual_recebido(self):
        """Calcula o percentual já recebido"""
        if self.valor_total > 0:
            return float((self.valor_recebido / self.valor_total) * 100)
        return 0.0
    
    def esta_recebido(self):
        """Verifica se está totalmente recebido"""
        return self.valor_recebido >= self.valor_total
    
    def esta_atrasado(self):
        """Verifica se está atrasado"""
        if self.status == 'RECEBIDO':
            return False
        from datetime import date
        if self.data_prevista:
            return self.data_prevista < date.today()
        return False
    
    def dias_ate_recebimento(self):
        """Calcula quantos dias faltam para o recebimento"""
        from datetime import date
        if self.data_prevista:
            delta = self.data_prevista - date.today()
            return delta.days
        return None
    
    def categoria_display(self):
        """Retorna o nome da categoria formatado"""
        return dict(self.CATEGORIA_CHOICES).get(self.categoria, self.categoria)
    
    def status_display(self):
        """Retorna o nome do status formatado"""
        return dict(self.STATUS_CHOICES).get(self.status, self.status)
    
    def mes_formatado(self):
        """Retorna o mês/ano da data prevista"""
        if self.data_prevista:
            meses_pt = {
                1: 'Janeiro', 2: 'Fevereiro', 3: 'Março', 4: 'Abril',
                5: 'Maio', 6: 'Junho', 7: 'Julho', 8: 'Agosto',
                9: 'Setembro', 10: 'Outubro', 11: 'Novembro', 12: 'Dezembro'
            }
            return f"{meses_pt[self.data_prevista.month]}/{self.data_prevista.year}"
        return "-"
    
    def get_categoria_color(self):
        """Retorna a cor apropriada para cada categoria"""
        cores = {
            'MENSALIDADE': '#10b981',      # Verde
            'INGRESSO': '#3b82f6',         # Azul
            'PATROCINIO': '#8b5cf6',       # Roxo
            'DOACAO': '#ec4899',           # Pink
            'WORKSHOP': '#f59e0b',         # Âmbar
            'ALUGUEL_ESPACO': '#14b8a6',   # Teal
            'APRESENTACAO': '#f43f5e',     # Rosa
            'MERCHANDISING': '#84cc16',    # Lima
            'CONSULTA': '#6366f1',         # Indigo
            'OUTRO': '#6b7280',            # Cinza
        }
        return cores.get(self.categoria, '#6b7280')
    
    def get_status_color(self):
        """Retorna a cor apropriada para o status"""
        cores = {
            'PENDENTE': '#f59e0b',    # Âmbar
            'RECEBIDO': '#22c55e',    # Verde
            'ATRASADO': '#ef4444',    # Vermelho
            'PARCIAL': '#3b82f6',     # Azul
            'CANCELADO': '#6b7280',   # Cinza
        }
        return cores.get(self.status, '#6b7280')
    
    def get_status_badge_class(self):
        """Retorna a classe Bootstrap para o badge de status"""
        classes = {
            'PENDENTE': 'bg-warning',
            'RECEBIDO': 'bg-success',
            'ATRASADO': 'bg-danger',
            'PARCIAL': 'bg-info',
            'CANCELADO': 'bg-secondary',
        }
        return classes.get(self.status, 'bg-secondary')
    
    def parcelas_display(self):
        """Retorna string formatada das parcelas"""
        if self.numero_parcelas and self.parcela_atual:
            return f"{self.parcela_atual}/{self.numero_parcelas}"
        return "-"





