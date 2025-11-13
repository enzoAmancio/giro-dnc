import os
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'giro_dance.settings')
django.setup()

from paginas.models import Aula

# Buscar e deletar o vídeo de teste
try:
    aula = Aula.objects.get(video='aulas/videos/Ballet_Iniciante/2025-11-08_TESTE.mp4')
    print(f"Encontrada aula: {aula.tema}")
    print(f"Turma: {aula.turma}")
    print(f"Data: {aula.data}")
    print(f"Arquivo de vídeo: {aula.video}")
    
    confirmacao = input("\nDeseja realmente deletar esta aula do banco de dados? (S/N): ")
    
    if confirmacao.upper() == 'S':
        aula.delete()
        print("✅ Aula deletada com sucesso do banco de dados!")
    else:
        print("❌ Operação cancelada.")
        
except Aula.DoesNotExist:
    print("❌ Aula com este vídeo não encontrada no banco de dados.")
except Exception as e:
    print(f"❌ Erro: {e}")

