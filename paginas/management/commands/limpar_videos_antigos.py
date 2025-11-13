from django.core.management.base import BaseCommand
from django.utils import timezone
from paginas.models import Aula
import os

class Command(BaseCommand):
    help = 'Remove vídeos de aulas com mais de X dias para liberar espaço no servidor'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dias',
            type=int,
            default=30,
            help='Número de dias para manter os vídeos (padrão: 30)'
        )
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Simula a execução sem deletar os arquivos'
        )

    def handle(self, *args, **options):
        dias = options['dias']
        dry_run = options['dry_run']
        
        # Data limite (aulas mais antigas que isso terão vídeos removidos)
        data_limite = timezone.now() - timezone.timedelta(days=dias)
        
        # Buscar aulas com vídeo mais antigas que a data limite
        aulas_antigas = Aula.objects.filter(
            data_upload_video__lt=data_limite,
            video__isnull=False
        ).exclude(video='')
        
        total_aulas = aulas_antigas.count()
        tamanho_total = 0
        
        self.stdout.write(self.style.WARNING(f'\n🔍 Buscando vídeos com mais de {dias} dias...'))
        self.stdout.write(f'   Data limite: {data_limite.strftime("%d/%m/%Y %H:%M")}\n')
        
        if total_aulas == 0:
            self.stdout.write(self.style.SUCCESS('✅ Nenhum vídeo antigo encontrado!'))
            return
        
        self.stdout.write(f'📹 Encontradas {total_aulas} aulas com vídeos antigos:\n')
        
        for aula in aulas_antigas:
            tamanho_mb = aula.get_video_size_mb()
            tamanho_total += tamanho_mb
            dias_upload = aula.dias_desde_upload()
            
            self.stdout.write(
                f'   • {aula.turma.nome} - {aula.data.strftime("%d/%m/%Y")} '
                f'({tamanho_mb:.2f} MB, {dias_upload} dias)'
            )
        
        self.stdout.write(f'\n💾 Espaço total a ser liberado: {tamanho_total:.2f} MB\n')
        
        if dry_run:
            self.stdout.write(self.style.WARNING('⚠️  DRY RUN - Nenhum arquivo foi deletado'))
            self.stdout.write('   Execute sem --dry-run para deletar os vídeos\n')
        else:
            # Confirmar antes de deletar
            confirmacao = input('⚠️  Deseja realmente deletar esses vídeos? (s/N): ')
            
            if confirmacao.lower() == 's':
                deletados = 0
                for aula in aulas_antigas:
                    try:
                        # Deletar o arquivo físico
                        if aula.video and os.path.isfile(aula.video.path):
                            os.remove(aula.video.path)
                        
                        # Limpar o campo no banco
                        aula.video = None
                        aula.save()
                        deletados += 1
                    except Exception as e:
                        self.stdout.write(
                            self.style.ERROR(f'❌ Erro ao deletar vídeo de {aula}: {str(e)}')
                        )
                
                self.stdout.write(
                    self.style.SUCCESS(f'\n✅ {deletados} vídeos deletados com sucesso!')
                )
                self.stdout.write(
                    self.style.SUCCESS(f'💾 {tamanho_total:.2f} MB liberados no servidor\n')
                )
            else:
                self.stdout.write(self.style.WARNING('\n❌ Operação cancelada\n'))
