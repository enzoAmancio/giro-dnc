from django.core.management.base import BaseCommand
from django.utils import timezone
from paginas.models import Mensalidade

class Command(BaseCommand):
    help = 'Atualiza o status das mensalidades vencidas para ATRASADO'

    def handle(self, *args, **options):
        hoje = timezone.now().date()
        
        # Buscar mensalidades pendentes e vencidas
        mensalidades_vencidas = Mensalidade.objects.filter(
            status='PENDENTE',
            data_vencimento__lt=hoje
        )
        
        count = mensalidades_vencidas.count()
        
        if count > 0:
            # Atualizar status para ATRASADO
            mensalidades_vencidas.update(status='ATRASADO')
            self.stdout.write(
                self.style.SUCCESS(f'✅ {count} mensalidade(s) atualizada(s) para ATRASADO')
            )
        else:
            self.stdout.write(
                self.style.SUCCESS('✅ Nenhuma mensalidade atrasada encontrada')
            )
