from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from paginas.models import Turma, Aluno, Aula, HorarioAula, Frequencia, Aviso, Mensalidade, Notificacao
from datetime import datetime, timedelta, time
from django.utils import timezone

class Command(BaseCommand):
    help = 'Popula o banco de dados com dados de teste'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('🚀 Iniciando população do banco de dados...'))
        
        # Criar professor
        professor, created = User.objects.get_or_create(
            username='professor',
            defaults={
                'first_name': 'Maria',
                'last_name': 'Silva',
                'email': 'maria@girodance.com'
            }
        )
        if created:
            professor.set_password('professor123')
            professor.save()
            self.stdout.write(self.style.SUCCESS(f'✅ Professor criado: {professor.username}'))
        
        # Criar turmas
        turmas_data = [
            {'nome': 'Ballet Iniciante', 'modalidade': 'BALLET', 'nivel': 'INICIANTE'},
            {'nome': 'Jazz Intermediário', 'modalidade': 'JAZZ', 'nivel': 'INTERMEDIARIO'},
            {'nome': 'Hip Hop Avançado', 'modalidade': 'HIP_HOP', 'nivel': 'AVANCADO'},
        ]
        
        turmas = []
        for data in turmas_data:
            turma, created = Turma.objects.get_or_create(
                nome=data['nome'],
                defaults={
                    'modalidade': data['modalidade'],
                    'nivel': data['nivel'],
                    'professor': professor,
                    'capacidade_maxima': 20,
                    'ativa': True,
                    'descricao': f'Turma de {data["nome"]}',
                    'data_inicio': datetime.now().date()
                }
            )
            turmas.append(turma)
            if created:
                self.stdout.write(self.style.SUCCESS(f'✅ Turma criada: {turma.nome}'))
        
        # Criar horários para as turmas
        dias = ['SEG', 'QUA', 'SEX']
        hora_inicio = time(18, 0)
        hora_fim = time(19, 30)
        
        for turma in turmas:
            for dia in dias:
                HorarioAula.objects.get_or_create(
                    turma=turma,
                    dia_semana=dia,
                    hora_inicio=hora_inicio,
                    defaults={
                        'hora_fim': hora_fim,
                        'sala': f'Sala {turmas.index(turma) + 1}'
                    }
                )
        self.stdout.write(self.style.SUCCESS('✅ Horários criados para todas as turmas'))
        
        # Buscar ou criar aluno associado ao usuário logado
        usuarios = User.objects.exclude(username='professor').exclude(is_superuser=True)
        
        for user in usuarios:
            aluno, created = Aluno.objects.get_or_create(
                usuario=user,
                defaults={
                    'cpf': f'{user.id:011d}',
                    'data_nascimento': datetime(2000, 1, 1).date(),
                    'telefone': '(11) 98765-4321',
                    'telefone_emergencia': '(11) 91234-5678',
                    'endereco': 'Rua das Danças, 123 - São Paulo/SP',
                    'ativo': True
                }
            )
            
            if created:
                # Associar aluno às turmas
                aluno.turmas.add(*turmas[:2])  # Adiciona às primeiras 2 turmas
                self.stdout.write(self.style.SUCCESS(f'✅ Aluno criado: {user.get_full_name() or user.username}'))
            
            # Criar aulas passadas (últimos 7 dias)
            hoje = datetime.now().date()
            for i in range(7):
                data_aula = hoje - timedelta(days=i)
                for turma in aluno.turmas.all():
                    aula, created = Aula.objects.get_or_create(
                        turma=turma,
                        data=data_aula,
                        hora_inicio=time(18, 0),
                        defaults={
                            'hora_fim': time(19, 30),
                            'tema': f'Aula de {turma.nome}',
                            'conteudo': 'Treino de coreografia e técnica',
                            'realizada': True
                        }
                    )
                    
                    if created:
                        # Criar frequência
                        Frequencia.objects.get_or_create(
                            aluno=aluno,
                            aula=aula,
                            defaults={
                                'status': 'PRESENTE' if i < 6 else 'FALTA',
                                'justificativa': 'Atestado médico' if i == 6 else ''
                            }
                        )
            
            # Criar aulas futuras (próximos 7 dias)
            for i in range(1, 8):
                data_aula = hoje + timedelta(days=i)
                for turma in aluno.turmas.all():
                    Aula.objects.get_or_create(
                        turma=turma,
                        data=data_aula,
                        hora_inicio=time(18, 0),
                        defaults={
                            'hora_fim': time(19, 30),
                            'tema': f'Próxima aula de {turma.nome}',
                            'conteudo': 'Preparação para apresentação',
                            'realizada': False
                        }
                    )
            
            self.stdout.write(self.style.SUCCESS(f'✅ Aulas criadas para {user.username}'))
            
            # Criar avisos
            avisos_data = [
                {
                    'titulo': 'Apresentação de fim de ano',
                    'conteudo': 'Não esqueçam da apresentação no dia 20/12!',
                    'tipo': 'GERAL',
                    'importante': True
                },
                {
                    'titulo': 'Nova coreografia',
                    'conteudo': 'Começaremos a ensaiar a nova coreografia na próxima aula.',
                    'tipo': 'TURMA',
                    'turma': turmas[0],
                    'importante': False
                },
                {
                    'titulo': 'Reposição de aula',
                    'conteudo': 'A aula do dia 15 será reposta no sábado.',
                    'tipo': 'GERAL',
                    'importante': False
                },
            ]
            
            for aviso_data in avisos_data:
                Aviso.objects.get_or_create(
                    titulo=aviso_data['titulo'],
                    defaults={
                        **aviso_data,
                        'autor': professor,
                        'ativo': True,
                        'data_criacao': timezone.now()
                    }
                )
            
            # Criar mensalidades
            for i in range(3):
                mes_ref = hoje.replace(day=1) - timedelta(days=30*i)
                status = 'PAGO' if i > 0 else 'PENDENTE'
                
                Mensalidade.objects.get_or_create(
                    aluno=aluno,
                    mes_referencia=mes_ref,
                    defaults={
                        'valor': 200.00,
                        'valor_desconto': 0.00,
                        'valor_final': 200.00,
                        'data_vencimento': mes_ref.replace(day=10),
                        'data_pagamento': mes_ref.replace(day=8) if status == 'PAGO' else None,
                        'status': status,
                        'forma_pagamento': 'PIX' if status == 'PAGO' else ''
                    }
                )
            
            self.stdout.write(self.style.SUCCESS(f'✅ Mensalidades criadas para {user.username}'))
        
            # Criar notificações
            notificacoes_data = [
                {
                    'tipo': 'AVISO',
                    'titulo': 'Nova aula disponível!',
                    'mensagem': 'Uma nova aula foi agendada para esta semana.',
                    'link': '/painel/minhas-aulas/'
                },
                {
                    'tipo': 'ALERTA',
                    'titulo': 'Mensalidade próxima do vencimento',
                    'mensagem': 'Sua mensalidade vence em 3 dias. Não esqueça de realizar o pagamento!',
                    'link': '/financeiro/mensalidades/'
                },
                {
                    'tipo': 'INFO',
                    'titulo': 'Atualização no horário',
                    'mensagem': 'Confira os novos horários de aula disponíveis.',
                    'link': '/painel/horarios/'
                },
                {
                    'tipo': 'SUCESSO',
                    'titulo': 'Pagamento confirmado',
                    'mensagem': 'Seu pagamento foi confirmado com sucesso!',
                    'link': '/financeiro/extrato/'
                },
            ]
            
            for notif_data in notificacoes_data:
                Notificacao.objects.get_or_create(
                    usuario=user,
                    titulo=notif_data['titulo'],
                    defaults={
                        **notif_data,
                        'lida': False
                    }
                )
            
            self.stdout.write(self.style.SUCCESS(f'✅ Notificações criadas para {user.username}'))
        
        self.stdout.write(self.style.SUCCESS('\n🎉 Banco de dados populado com sucesso!'))
        self.stdout.write(self.style.WARNING('\n📊 Resumo:'))
        self.stdout.write(f'  - {Turma.objects.count()} turmas')
        self.stdout.write(f'  - {Aluno.objects.count()} alunos')
        self.stdout.write(f'  - {Aula.objects.count()} aulas')
        self.stdout.write(f'  - {Frequencia.objects.count()} registros de frequência')
        self.stdout.write(f'  - {Aviso.objects.count()} avisos')
        self.stdout.write(f'  - {Mensalidade.objects.count()} mensalidades')
        self.stdout.write(f'  - {Notificacao.objects.count()} notificações')
