"""
Management command para popular o banco de dados com dados de exemplo
Uso: python manage.py popular_dados
"""

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from painel_aluno_app.models import (
    Aluno, Turma, Aula, HorarioAula, Frequencia,
    Aviso, Mensalidade, Mensagem
)
from datetime import datetime, timedelta, time
from decimal import Decimal
import random


class Command(BaseCommand):
    help = 'Popula o banco de dados com dados de exemplo para testes'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Limpa os dados existentes antes de popular',
        )

    def handle(self, *args, **options):
        if options['clear']:
            self.stdout.write(self.style.WARNING('Limpando dados existentes...'))
            self.limpar_dados()

        self.stdout.write(self.style.SUCCESS('Iniciando população do banco de dados...'))

        # Criar usuários
        self.stdout.write('Criando usuários...')
        usuarios = self.criar_usuarios()

        # Criar turmas
        self.stdout.write('Criando turmas...')
        turmas = self.criar_turmas(usuarios['professores'])

        # Criar horários
        self.stdout.write('Criando horários de aulas...')
        self.criar_horarios(turmas)

        # Criar alunos
        self.stdout.write('Criando alunos...')
        alunos = self.criar_alunos(usuarios['alunos'], turmas)

        # Criar aulas
        self.stdout.write('Criando aulas...')
        aulas = self.criar_aulas(turmas)

        # Criar frequências
        self.stdout.write('Criando frequências...')
        self.criar_frequencias(alunos, aulas)

        # Criar avisos
        self.stdout.write('Criando avisos...')
        self.criar_avisos(usuarios['professores'], turmas, alunos)

        # Criar mensalidades
        self.stdout.write('Criando mensalidades...')
        self.criar_mensalidades(alunos)

        # Criar mensagens
        self.stdout.write('Criando mensagens...')
        self.criar_mensagens(usuarios['alunos'], usuarios['professores'])

        self.stdout.write(self.style.SUCCESS('✅ Banco de dados populado com sucesso!'))
        self.stdout.write(self.style.SUCCESS('\nUsuários criados:'))
        self.stdout.write(f'  Professores: {len(usuarios["professores"])}')
        self.stdout.write(f'  Alunos: {len(usuarios["alunos"])}')
        self.stdout.write(self.style.SUCCESS(f'\nTurmas: {len(turmas)}'))
        self.stdout.write(self.style.SUCCESS(f'Aulas: {len(aulas)}'))
        self.stdout.write(self.style.SUCCESS(f'Alunos cadastrados: {len(alunos)}'))
        
        self.stdout.write('\n' + '='*50)
        self.stdout.write('Credenciais de teste:')
        self.stdout.write('='*50)
        self.stdout.write('Aluno 1: aluno1 / senha123')
        self.stdout.write('Aluno 2: aluno2 / senha123')
        self.stdout.write('Professor: prof1 / senha123')
        self.stdout.write('Admin: admin / admin123')
        self.stdout.write('='*50)

    def limpar_dados(self):
        """Limpa todos os dados de teste"""
        Mensagem.objects.all().delete()
        Mensalidade.objects.all().delete()
        Aviso.objects.all().delete()
        Frequencia.objects.all().delete()
        Aula.objects.all().delete()
        HorarioAula.objects.all().delete()
        Aluno.objects.all().delete()
        Turma.objects.all().delete()
        User.objects.filter(is_superuser=False).delete()

    def criar_usuarios(self):
        """Cria usuários de exemplo"""
        # Criar superusuário se não existir
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser(
                username='admin',
                email='admin@girodnc.com',
                password='admin123',
                first_name='Administrador',
                last_name='Sistema'
            )

        # Criar professores
        professores = []
        nomes_profs = [
            ('Maria', 'Silva', 'maria.silva@girodnc.com'),
            ('João', 'Santos', 'joao.santos@girodnc.com'),
            ('Ana', 'Costa', 'ana.costa@girodnc.com'),
        ]

        for i, (primeiro, ultimo, email) in enumerate(nomes_profs, 1):
            if not User.objects.filter(username=f'prof{i}').exists():
                prof = User.objects.create_user(
                    username=f'prof{i}',
                    email=email,
                    password='senha123',
                    first_name=primeiro,
                    last_name=ultimo
                )
                professores.append(prof)

        # Criar alunos
        alunos = []
        nomes_alunos = [
            ('Pedro', 'Oliveira', 'pedro.oliveira@email.com'),
            ('Julia', 'Ferreira', 'julia.ferreira@email.com'),
            ('Lucas', 'Almeida', 'lucas.almeida@email.com'),
            ('Beatriz', 'Lima', 'beatriz.lima@email.com'),
            ('Gabriel', 'Rodrigues', 'gabriel.rodrigues@email.com'),
            ('Camila', 'Pereira', 'camila.pereira@email.com'),
            ('Rafael', 'Souza', 'rafael.souza@email.com'),
            ('Amanda', 'Carvalho', 'amanda.carvalho@email.com'),
        ]

        for i, (primeiro, ultimo, email) in enumerate(nomes_alunos, 1):
            if not User.objects.filter(username=f'aluno{i}').exists():
                aluno = User.objects.create_user(
                    username=f'aluno{i}',
                    email=email,
                    password='senha123',
                    first_name=primeiro,
                    last_name=ultimo
                )
                alunos.append(aluno)

        return {'professores': professores, 'alunos': alunos}

    def criar_turmas(self, professores):
        """Cria turmas de exemplo"""
        turmas_dados = [
            ('Ballet Iniciante A', 'BALLET', 'INICIANTE', 15),
            ('Ballet Intermediário', 'BALLET', 'INTERMEDIARIO', 12),
            ('Jazz Iniciante', 'JAZZ', 'INICIANTE', 20),
            ('Hip Hop Avançado', 'HIP_HOP', 'AVANCADO', 15),
            ('Dança Contemporânea', 'CONTEMPORANEO', 'INTERMEDIARIO', 18),
            ('Street Dance', 'STREET_DANCE', 'INICIANTE', 20),
        ]

        turmas = []
        for nome, modalidade, nivel, capacidade in turmas_dados:
            professor = random.choice(professores)
            turma = Turma.objects.create(
                nome=nome,
                modalidade=modalidade,
                nivel=nivel,
                professor=professor,
                capacidade_maxima=capacidade,
                ativa=True,
                descricao=f'Turma de {modalidade.replace("_", " ").title()} - Nível {nivel}',
                data_inicio=datetime.now().date() - timedelta(days=90),
                data_fim=datetime.now().date() + timedelta(days=180)
            )
            turmas.append(turma)

        return turmas

    def criar_horarios(self, turmas):
        """Cria horários para as turmas"""
        dias = ['SEG', 'TER', 'QUA', 'QUI', 'SEX', 'SAB']
        horarios = [
            (time(9, 0), time(10, 30)),
            (time(14, 0), time(15, 30)),
            (time(16, 0), time(17, 30)),
            (time(18, 0), time(19, 30)),
            (time(19, 30), time(21, 0)),
        ]
        salas = ['Sala 1', 'Sala 2', 'Sala 3', 'Estúdio Principal']

        for turma in turmas:
            # Cada turma tem 2 ou 3 horários por semana
            num_horarios = random.randint(2, 3)
            dias_escolhidos = random.sample(dias, num_horarios)

            for dia in dias_escolhidos:
                hora_inicio, hora_fim = random.choice(horarios)
                sala = random.choice(salas)

                HorarioAula.objects.create(
                    turma=turma,
                    dia_semana=dia,
                    hora_inicio=hora_inicio,
                    hora_fim=hora_fim,
                    sala=sala
                )

    def criar_alunos(self, usuarios_alunos, turmas):
        """Cria perfis de alunos"""
        alunos = []
        base_cpf = 12345678900

        for i, usuario in enumerate(usuarios_alunos, 1):
            # Data de nascimento aleatória (15 a 45 anos atrás)
            dias_atras = random.randint(15*365, 45*365)
            data_nascimento = datetime.now().date() - timedelta(days=dias_atras)

            aluno = Aluno.objects.create(
                usuario=usuario,
                cpf=f'{base_cpf + i:011d}',
                data_nascimento=data_nascimento,
                telefone=f'(11) 9{random.randint(1000, 9999)}-{random.randint(1000, 9999)}',
                telefone_emergencia=f'(11) 9{random.randint(1000, 9999)}-{random.randint(1000, 9999)}',
                endereco=f'Rua Exemplo, {random.randint(1, 999)} - São Paulo, SP',
                ativo=True,
                observacoes='Aluno regular'
            )

            # Matricular em 1 ou 2 turmas aleatórias
            turmas_aluno = random.sample(list(turmas), random.randint(1, 2))
            aluno.turmas.set(turmas_aluno)

            alunos.append(aluno)

        return alunos

    def criar_aulas(self, turmas):
        """Cria aulas para as turmas"""
        aulas = []
        hoje = datetime.now().date()

        # Criar aulas dos últimos 60 dias
        for turma in turmas:
            horarios = turma.horarios.all()

            for dias_atras in range(60, -1, -1):
                data_aula = hoje - timedelta(days=dias_atras)
                dia_semana = ['SEG', 'TER', 'QUA', 'QUI', 'SEX', 'SAB', 'DOM'][data_aula.weekday()]

                # Verificar se há horário para este dia
                horarios_dia = horarios.filter(dia_semana=dia_semana)

                for horario in horarios_dia:
                    # 90% de chance de a aula ter sido realizada
                    realizada = random.random() < 0.9 if dias_atras > 0 else False

                    aula = Aula.objects.create(
                        turma=turma,
                        data=data_aula,
                        hora_inicio=horario.hora_inicio,
                        hora_fim=horario.hora_fim,
                        tema=f'Aula de {turma.modalidade.replace("_", " ").title()}',
                        conteudo='Aquecimento, exercícios técnicos e coreografia',
                        realizada=realizada
                    )
                    aulas.append(aula)

        # Criar aulas futuras (próximos 14 dias)
        for turma in turmas:
            horarios = turma.horarios.all()

            for dias_futuros in range(1, 15):
                data_aula = hoje + timedelta(days=dias_futuros)
                dia_semana = ['SEG', 'TER', 'QUA', 'QUI', 'SEX', 'SAB', 'DOM'][data_aula.weekday()]

                horarios_dia = horarios.filter(dia_semana=dia_semana)

                for horario in horarios_dia:
                    aula = Aula.objects.create(
                        turma=turma,
                        data=data_aula,
                        hora_inicio=horario.hora_inicio,
                        hora_fim=horario.hora_fim,
                        tema=f'Aula de {turma.modalidade.replace("_", " ").title()}',
                        conteudo='Previsto: Aquecimento, exercícios técnicos e coreografia',
                        realizada=False
                    )
                    aulas.append(aula)

        return aulas

    def criar_frequencias(self, alunos, aulas):
        """Cria registros de frequência"""
        hoje = datetime.now().date()

        for aluno in alunos:
            turmas_aluno = aluno.turmas.all()

            # Buscar aulas realizadas das turmas do aluno
            aulas_aluno = Aula.objects.filter(
                turma__in=turmas_aluno,
                realizada=True,
                data__lte=hoje
            )

            for aula in aulas_aluno:
                # 85% de presença, 10% falta, 5% falta justificada
                rand = random.random()
                if rand < 0.85:
                    status = 'PRESENTE'
                elif rand < 0.95:
                    status = 'FALTA'
                else:
                    status = 'FALTA_JUSTIFICADA'

                justificativa = ''
                if status == 'FALTA_JUSTIFICADA':
                    justificativa = random.choice([
                        'Atestado médico',
                        'Compromisso familiar',
                        'Viagem',
                        'Problema pessoal'
                    ])

                Frequencia.objects.create(
                    aluno=aluno,
                    aula=aula,
                    status=status,
                    justificativa=justificativa
                )

    def criar_avisos(self, professores, turmas, alunos):
        """Cria avisos de exemplo"""
        hoje = datetime.now()

        avisos_dados = [
            ('Recesso de fim de ano', 'Informamos que teremos recesso de 20/12 a 05/01. Feliz Natal e Ano Novo!', 'GERAL', True),
            ('Apresentação de final de ano', 'Não percam nossa apresentação de final de ano dia 15/12 às 19h no Teatro Municipal!', 'EVENTO', True),
            ('Reposição de aula', 'A aula de quinta-feira será reposta no sábado às 14h.', 'TURMA', False),
            ('Uniforme obrigatório', 'Lembramos que o uso do uniforme é obrigatório em todas as aulas.', 'GERAL', False),
            ('Nova coreografia', 'Iniciamos nova coreografia nesta semana. Não faltem!', 'TURMA', False),
        ]

        for titulo, conteudo, tipo, importante in avisos_dados:
            autor = random.choice(professores)
            turma = random.choice(turmas) if tipo == 'TURMA' else None
            aluno = random.choice(alunos) if tipo == 'ALUNO' else None

            Aviso.objects.create(
                titulo=titulo,
                conteudo=conteudo,
                tipo=tipo,
                autor=autor,
                turma=turma,
                aluno=aluno,
                importante=importante,
                ativo=True,
                data_expiracao=hoje + timedelta(days=30)
            )

    def criar_mensalidades(self, alunos):
        """Cria mensalidades para os alunos"""
        hoje = datetime.now().date()

        # Criar mensalidades dos últimos 6 meses e próximos 3 meses
        for aluno in alunos:
            num_turmas = aluno.turmas.count()
            valor_base = Decimal('150.00') * num_turmas

            for meses_atras in range(6, -4, -1):
                mes_ref = hoje.replace(day=1) + timedelta(days=30 * meses_atras)
                mes_ref = mes_ref.replace(day=1)

                vencimento = mes_ref.replace(day=10)

                # Determinar status
                if vencimento < hoje:
                    if random.random() < 0.8:  # 80% pagos
                        status = 'PAGO'
                        data_pagamento = vencimento + timedelta(days=random.randint(0, 5))
                    else:
                        status = 'ATRASADO'
                        data_pagamento = None
                else:
                    status = 'PENDENTE'
                    data_pagamento = None

                # Desconto aleatório para alguns
                desconto = Decimal('0.00')
                if random.random() < 0.2:  # 20% com desconto
                    desconto = valor_base * Decimal('0.1')  # 10% de desconto

                Mensalidade.objects.create(
                    aluno=aluno,
                    mes_referencia=mes_ref,
                    valor=valor_base,
                    valor_desconto=desconto,
                    valor_final=valor_base - desconto,
                    data_vencimento=vencimento,
                    data_pagamento=data_pagamento,
                    status=status,
                    forma_pagamento='PIX' if status == 'PAGO' else ''
                )

    def criar_mensagens(self, alunos, professores):
        """Cria mensagens de exemplo"""
        hoje = datetime.now()

        assuntos = [
            'Dúvida sobre horário',
            'Falta justificada',
            'Troca de horário',
            'Dúvida sobre coreografia',
            'Pedido de reposição',
        ]

        conteudos = [
            'Olá, gostaria de tirar uma dúvida sobre o horário da próxima aula.',
            'Não poderei comparecer na próxima aula devido a um compromisso.',
            'Seria possível trocar meu horário de aula?',
            'Tenho uma dúvida sobre a coreografia que estamos ensaiando.',
            'Gostaria de repor a aula que perdi semana passada.',
        ]

        # Criar algumas mensagens
        for _ in range(15):
            remetente = random.choice(alunos)
            destinatario = random.choice(professores)
            assunto = random.choice(assuntos)
            conteudo = random.choice(conteudos)

            dias_atras = random.randint(0, 30)
            data_envio = hoje - timedelta(days=dias_atras)

            lida = random.random() < 0.6  # 60% lidas
            data_leitura = data_envio + timedelta(hours=random.randint(1, 48)) if lida else None

            Mensagem.objects.create(
                remetente=remetente,
                destinatario=destinatario,
                assunto=assunto,
                conteudo=conteudo,
                lida=lida,
                data_leitura=data_leitura
            )
