# 📹 Sistema de Upload de Vídeos - Documentação

## ✅ Implementado com Sucesso!

Sistema completo de upload de vídeos das aulas com **proteção contra sobrecarga** do servidor Oracle Cloud.

---

## 🎯 Funcionalidades Implementadas

### 1. **Upload de Vídeos com Limites**
- ✅ Tamanho máximo: **50MB por vídeo**
- ✅ Formatos aceitos: **MP4, WebM, AVI, MOV**
- ✅ Validação automática no upload
- ✅ Mensagem de erro clara se ultrapassar o limite

### 2. **Armazenamento Inteligente**
- ✅ Vídeos organizados por turma e data: `aulas/videos/{turma}/{data_tema}.mp4`
- ✅ Nomes de arquivo sanitizados (sem caracteres especiais)
- ✅ Data de upload registrada automaticamente

### 3. **Visualização para Alunos**
- ✅ **Próximas Aulas**: Mostra apenas aulas futuras (não realizadas)
- ✅ **Vídeos Recentes**: Últimas 5 aulas com vídeo disponível
- ✅ Player HTML5 integrado (sem plugins necessários)
- ✅ Botão de download para cada vídeo
- ✅ Informações: turma, data, horário, tema, tamanho do arquivo

### 4. **Painel Admin Aprimorado**
- ✅ Dashboard com estatísticas:
  - Total de vídeos armazenados
  - Espaço utilizado (MB e GB)
  - Vídeos antigos (>30 dias)
- ✅ Alertas visuais para vídeos antigos
- ✅ Colunas extras: "Tem vídeo?", "Tamanho", "Dias desde upload"

### 5. **Limpeza Automática**
- ✅ Comando para deletar vídeos antigos
- ✅ Configurável (padrão: 30 dias)
- ✅ Modo seguro (dry-run) para testar antes
- ✅ Confirmação antes de deletar

---

## 📋 Como Usar

### **Para Professores/Administradores**

#### 1. Fazer Upload de Vídeo
1. Acesse o **Django Admin**: `/admin/`
2. Vá em **Paginas → Aulas**
3. Clique na aula desejada ou crie uma nova
4. No campo **"Vídeo da aula"**, faça o upload do arquivo
5. Marque a aula como **"Realizada"**
6. Salve

**⚠️ IMPORTANTE**: O vídeo deve ter no máximo 50MB!

#### 2. Verificar Espaço Utilizado
1. Acesse **Django Admin → Paginas → Aulas**
2. No topo da página você verá:
   - 📊 Total de vídeos
   - 💾 Espaço utilizado
   - ⚠️ Vídeos antigos

#### 3. Limpar Vídeos Antigos

**Testar sem deletar (recomendado primeiro):**
```bash
python manage.py limpar_videos_antigos --dry-run
```

**Deletar vídeos com mais de 30 dias:**
```bash
python manage.py limpar_videos_antigos
```

**Deletar vídeos com mais de 60 dias:**
```bash
python manage.py limpar_videos_antigos --dias 60
```

**Deletar vídeos com mais de 15 dias:**
```bash
python manage.py limpar_videos_antigos --dias 15
```

### **Para Alunos**

#### Ver Vídeos das Aulas
1. Acesse o portal do aluno
2. Vá em **"Horários de aula"**
3. Role até a seção **"Vídeos das Últimas Aulas"**
4. Clique no play para assistir
5. Ou clique em **"Baixar"** para fazer download

---

## 🛡️ Proteções Implementadas

### 1. **Limite de Tamanho**
```python
# Máximo 50MB por vídeo
def validate_video_size(value):
    max_size_mb = 50
    # Valida e retorna erro se ultrapassar
```

### 2. **Formatos Permitidos**
```python
FileExtensionValidator(
    allowed_extensions=['mp4', 'webm', 'avi', 'mov']
)
```

### 3. **Limpeza Automática**
- Vídeos antigos podem ser deletados manualmente
- Recomendação: executar mensalmente

### 4. **Deleção em Cascata**
- Se deletar uma aula, o vídeo é automaticamente removido do servidor

---

## 📊 Monitoramento de Espaço

### No Django Admin:
```
📹 Estatísticas de Vídeos
┌─────────────────────┬─────────────────────┬─────────────────────┐
│   Total de Vídeos   │  Espaço Utilizado   │   Vídeos Antigos    │
│         25          │    1234 MB (1.2GB)  │          8          │
└─────────────────────┴─────────────────────┴─────────────────────┘

💡 Dica: Execute python manage.py limpar_videos_antigos para liberar espaço
```

### Via Comando:
```bash
python manage.py limpar_videos_antigos --dry-run

# Saída:
🔍 Buscando vídeos com mais de 30 dias...
   Data limite: 05/10/2025 10:30

📹 Encontradas 8 aulas com vídeos antigos:

   • Ballet Iniciante - 15/09/2025 (45.30 MB, 52 dias)
   • Jazz Avançado - 20/09/2025 (38.12 MB, 47 dias)
   ...

💾 Espaço total a ser liberado: 342.56 MB
```

---

## 💡 Recomendações

### **Para Evitar Consumo Excessivo:**

1. **Limite de Vídeos por Turma**
   - Manter apenas os últimos 2-3 vídeos por turma
   - Executar limpeza mensalmente

2. **Otimizar Vídeos Antes do Upload**
   - Comprimir vídeos usando HandBrake ou similar
   - Resolução recomendada: 720p (1280x720)
   - Bitrate recomendado: 1500-2500 kbps

3. **Ferramentas de Compressão Gratuitas:**
   - **HandBrake** (Windows/Mac/Linux)
   - **FFmpeg** (linha de comando)
   - **Online**: https://www.freeconvert.com/video-compressor

4. **Exemplo de Compressão com FFmpeg:**
```bash
ffmpeg -i video_original.mp4 -vcodec h264 -acodec aac -b:v 2000k -b:a 128k video_comprimido.mp4
```

5. **Agenda de Limpeza Sugerida:**
   - Vídeos com mais de 30 dias: Deletar mensalmente
   - Manter apenas vídeos importantes (revisões, coreografias especiais)

---

## 🚀 Próximos Passos (Opcional)

### Se Precisar de Mais Otimização:

1. **Compressão Automática no Upload**
   - Processar vídeos automaticamente ao fazer upload
   - Reduzir resolução e bitrate

2. **Integração com Serviços Externos**
   - YouTube (privado/não listado)
   - Vimeo
   - Google Drive
   - AWS S3 (pago)

3. **Streaming Adaptativo**
   - HLS ou DASH para melhor performance
   - Carregamento progressivo

---

## 📁 Arquivos Modificados

1. **`paginas/models.py`**
   - Campo `video` adicionado ao modelo `Aula`
   - Validadores de tamanho e formato
   - Métodos auxiliares

2. **`paginas/views.py`**
   - View `painel_aluno_horarios` atualizada
   - Filtros para próximas aulas e vídeos

3. **`paginas/templates/painel/horarios_aula.html`**
   - Seção de próximas aulas
   - Galeria de vídeos com player HTML5

4. **`paginas/admin.py`**
   - Estatísticas de vídeos
   - Colunas extras na lista

5. **`paginas/management/commands/limpar_videos_antigos.py`**
   - Comando de limpeza automática

6. **`paginas/templates/admin/paginas/aula/change_list.html`**
   - Dashboard de estatísticas no admin

---

## ❓ FAQ

**P: O que acontece se eu tentar fazer upload de um vídeo maior que 50MB?**
R: O Django retorna erro: "O tamanho máximo do arquivo é 50MB. Seu arquivo tem XX MB."

**P: Os alunos podem fazer download dos vídeos?**
R: Sim, há um botão "Baixar" em cada vídeo.

**P: Como aumentar o limite de 50MB?**
R: Edite `paginas/models.py`, função `validate_video_size()`, linha `max_size_mb = 50`

**P: Posso usar outros formatos de vídeo?**
R: Sim, edite `paginas/models.py`, adicione na lista: `allowed_extensions=['mp4', 'webm', 'avi', 'mov', 'mkv']`

**P: Os vídeos são deletados automaticamente?**
R: Não, você precisa executar manualmente: `python manage.py limpar_videos_antigos`

**P: Como agendar limpeza automática?**
R: Use cron (Linux) ou Task Scheduler (Windows):
```bash
# Cron (Linux): Todo dia 1º do mês às 3h
0 3 1 * * cd /caminho/projeto && python manage.py limpar_videos_antigos --dias 30
```

---

## 🎓 Suporte

Se precisar de ajuda ou tiver dúvidas, consulte este documento ou entre em contato.

**Versão**: 1.0
**Data**: Novembro 2025
**Status**: ✅ Produção
