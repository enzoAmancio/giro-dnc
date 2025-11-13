# 🎬 Exemplo de Uso - Sistema de Vídeos

## 📸 Como Ficou a Página do Aluno

```
┌─────────────────────────────────────────────────────────────────┐
│  GIRO DNC - Horários de aula                                    │
└─────────────────────────────────────────────────────────────────┘

📅 PRÓXIMAS AULAS
┌──────────────────────┬──────────────────────┬──────────────────────┐
│  07/11/2025 (Qui)    │  08/11/2025 (Sex)    │  09/11/2025 (Sab)    │
│                      │                      │                      │
│  BALLET              │  JAZZ                │  HIP HOP             │
│  Turma: Iniciante A  │  Turma: Avançado B   │  Turma: Intermediário│
│  14:00 - 15:30       │  18:00 - 19:30       │  10:00 - 11:30       │
│  Tema: Alongamento   │  Tema: Coreografia 3 │  Tema: Freestyle     │
└──────────────────────┴──────────────────────┴──────────────────────┘

🕒 GRADE DE HORÁRIOS
┌─────────────┬─────────────┬─────────────┬─────────────┬─────────────┐
│ Segunda     │ Terça       │ Quarta      │ Quinta      │ Sexta       │
│ 14:00-15:30 │ 14:00-15:30 │ 14:00-15:30 │ 14:00-15:30 │ 18:00-19:30 │
│ BALLET      │ BALLET      │ BALLET      │ BALLET      │ JAZZ        │
│ Iniciante A │ Iniciante A │ Iniciante A │ Iniciante A │ Avançado B  │
└─────────────┴─────────────┴─────────────┴─────────────┴─────────────┘

📹 VÍDEOS DAS ÚLTIMAS AULAS
┌───────────────────────────────────────┬───────────────────────────────────────┐
│ 🎥 Ballet Iniciante A - 05/11/2025    │ 🎥 Jazz Avançado B - 04/11/2025       │
│ ┌─────────────────────────────────┐   │ ┌─────────────────────────────────┐   │
│ │                                 │   │ │                                 │   │
│ │     ▶️  PLAYER DE VÍDEO         │   │ │     ▶️  PLAYER DE VÍDEO         │   │
│ │                                 │   │ │                                 │   │
│ │   [━━━━━━━━━━━━━━━○━━━━━]      │   │ │   [━━━━━━━━━━━━━━━○━━━━━]      │   │
│ │   🔊 ⏸️  ⏩  ⏪  🔄  ⛶          │   │ │   🔊 ⏸️  ⏩  ⏪  🔄  ⛶          │   │
│ └─────────────────────────────────┘   │ └─────────────────────────────────┘   │
│                                       │                                       │
│ Tema: Postura e Equilíbrio            │ Tema: Técnica de Giros               │
│ 14:00 - 15:30 | 42.3 MB               │ 18:00 - 19:30 | 38.7 MB               │
│                                       │                                       │
│ [⬇️ Baixar]                            │ [⬇️ Baixar]                           │
└───────────────────────────────────────┴───────────────────────────────────────┘
```

---

## 🎯 Fluxo de Upload (Admin)

```
1. Professor acessa Django Admin
   └─> /admin/paginas/aula/

2. Clica em uma aula ou cria nova
   └─> Formulário de Aula

3. Preenche os dados:
   ┌─────────────────────────────────────┐
   │ Turma: [Ballet Iniciante A ▼]       │
   │ Data:  [05/11/2025] 📅              │
   │ Horário: [14:00] até [15:30]        │
   │ Tema:  [Postura e Equilíbrio]       │
   │                                     │
   │ 📹 Vídeo da aula:                   │
   │ [Escolher arquivo] video_aula.mp4   │
   │ ⚠️ Máximo 50MB | MP4, WebM, AVI     │
   │                                     │
   │ ✅ Realizada                        │
   └─────────────────────────────────────┘

4. Clica em [Salvar]
   └─> Sistema valida tamanho
       └─> Se > 50MB: ❌ ERRO
       └─> Se <= 50MB: ✅ Upload OK

5. Vídeo armazenado em:
   media/aulas/videos/Ballet_Iniciante_A/2025-11-05_Postura_e_Equilibrio.mp4
```

---

## 📊 Dashboard Admin

```
┌──────────────────────────────────────────────────────────────────────┐
│  Django Administration - Aulas                                       │
├──────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  📹 Estatísticas de Vídeos                                           │
│  ┌─────────────────┬────────────────────────┬────────────────────┐  │
│  │ Total de Vídeos │   Espaço Utilizado     │  Vídeos Antigos    │  │
│  │                 │                        │                    │  │
│  │       25        │    1234 MB (1.21 GB)   │         8          │  │
│  └─────────────────┴────────────────────────┴────────────────────┘  │
│                                                                      │
│  💡 Dica: Execute python manage.py limpar_videos_antigos            │
│           para liberar espaço no servidor.                          │
│                                                                      │
├──────────────────────────────────────────────────────────────────────┤
│  Filtros: [Todas] [Realizadas] [Não Realizadas] [Com Vídeo]         │
│  Buscar: [_____________________________________] 🔍                  │
├──────────────────────────────────────────────────────────────────────┤
│ Turma        │ Data       │ Horário │ Tema      │ ✓ │ Vídeo │ Tam   │
├──────────────┼────────────┼─────────┼───────────┼───┼───────┼───────┤
│ Ballet Inic. │ 05/11/2025 │ 14:00   │ Postura   │ ✓ │ ✓ Sim │ 42 MB │
│ Jazz Avanç.  │ 04/11/2025 │ 18:00   │ Giros     │ ✓ │ ✓ Sim │ 38 MB │
│ Hip Hop Int. │ 03/11/2025 │ 10:00   │ Freestyle │ ✓ │ ✗ Não │   -   │
└──────────────┴────────────┴─────────┴───────────┴───┴───────┴───────┘
```

---

## 🧹 Comando de Limpeza

```bash
$ python manage.py limpar_videos_antigos --dry-run

🔍 Buscando vídeos com mais de 30 dias...
   Data limite: 05/10/2025 10:30

📹 Encontradas 8 aulas com vídeos antigos:

   • Ballet Iniciante A - 15/09/2025 (45.30 MB, 52 dias)
   • Jazz Avançado B - 20/09/2025 (38.12 MB, 47 dias)
   • Hip Hop Intermediário - 22/09/2025 (41.50 MB, 45 dias)
   • Ballet Avançado C - 25/09/2025 (39.80 MB, 42 dias)
   • Street Dance - 28/09/2025 (44.20 MB, 39 dias)
   • Contemporâneo - 30/09/2025 (42.60 MB, 37 dias)
   • Dança de Salão - 01/10/2025 (40.10 MB, 35 dias)
   • Zumba - 03/10/2025 (50.94 MB, 33 dias)

💾 Espaço total a ser liberado: 342.56 MB

⚠️  DRY RUN - Nenhum arquivo foi deletado
   Execute sem --dry-run para deletar os vídeos
```

```bash
$ python manage.py limpar_videos_antigos

🔍 Buscando vídeos com mais de 30 dias...
   Data limite: 05/10/2025 10:30

📹 Encontradas 8 aulas com vídeos antigos:
   [... lista ...]

💾 Espaço total a ser liberado: 342.56 MB

⚠️  Deseja realmente deletar esses vídeos? (s/N): s

✅ 8 vídeos deletados com sucesso!
💾 342.56 MB liberados no servidor
```

---

## 🎨 Estrutura de Arquivos Criada

```
giro-dnc/
├── media/                           # Pasta de uploads (criada automaticamente)
│   └── aulas/
│       └── videos/
│           ├── Ballet_Iniciante_A/
│           │   ├── 2025-11-05_Postura_e_Equilibrio.mp4
│           │   └── 2025-11-01_Alongamento_Basico.mp4
│           ├── Jazz_Avancado_B/
│           │   └── 2025-11-04_Tecnica_de_Giros.mp4
│           └── Hip_Hop_Intermediario/
│               └── 2025-11-03_Freestyle_Avancado.mp4
│
├── paginas/
│   ├── models.py                    # ✨ Modelo Aula atualizado
│   ├── views.py                     # ✨ View atualizada
│   ├── admin.py                     # ✨ Admin com estatísticas
│   ├── management/
│   │   └── commands/
│   │       └── limpar_videos_antigos.py  # ✨ NOVO
│   └── templates/
│       ├── painel/
│       │   └── horarios_aula.html   # ✨ Template atualizado
│       └── admin/
│           └── paginas/
│               └── aula/
│                   └── change_list.html  # ✨ NOVO
│
└── SISTEMA_VIDEOS_README.md         # ✨ Documentação completa
```

---

## 💾 Exemplo de Consumo de Espaço

### Cenário 1: Uso Conservador
```
- 4 turmas
- 2 aulas por semana cada = 8 aulas/semana
- Vídeo médio: 40MB
- Manter 30 dias

Cálculo:
8 aulas × 4 semanas = 32 vídeos
32 vídeos × 40MB = 1.28 GB/mês ✅ SEGURO
```

### Cenário 2: Uso Moderado
```
- 8 turmas
- 3 aulas por semana cada = 24 aulas/semana
- Vídeo médio: 45MB
- Manter 30 dias

Cálculo:
24 aulas × 4 semanas = 96 vídeos
96 vídeos × 45MB = 4.32 GB/mês ⚠️ MODERADO
```

### Cenário 3: Uso Intenso
```
- 12 turmas
- 4 aulas por semana cada = 48 aulas/semana
- Vídeo médio: 50MB
- Manter 60 dias

Cálculo:
48 aulas × 8 semanas = 384 vídeos
384 vídeos × 50MB = 19.2 GB/2 meses ❌ CRÍTICO
```

**Recomendação**: Cenário 1 ou 2, com limpeza automática aos 30 dias.

---

## 🔧 Ajustes de Limite (se necessário)

### Aumentar para 100MB:
```python
# paginas/models.py, linha ~10
def validate_video_size(value):
    max_size_mb = 100  # ← Alterar aqui
    # ...
```

### Reduzir para 30MB:
```python
# paginas/models.py, linha ~10
def validate_video_size(value):
    max_size_mb = 30  # ← Alterar aqui
    # ...
```

### Aceitar MKV:
```python
# paginas/models.py, linha ~157
FileExtensionValidator(
    allowed_extensions=['mp4', 'webm', 'avi', 'mov', 'mkv']  # ← Adicionar 'mkv'
)
```

Após alterações, execute:
```bash
python manage.py makemigrations
python manage.py migrate
```

---

Pronto! Sistema de vídeos implementado e documentado! 🎉
