# Backend do Portal do Aluno - GIRO DNC

## 📋 Visão Geral

Este documento descreve o backend desenvolvido em Django para o Portal do Aluno da GIRO DNC.

## 🗄️ Modelos (Models)

### 1. **Turma**
Representa uma turma de dança.

**Campos:**
- `nome`: Nome da turma
- `modalidade`: Tipo de dança (Ballet, Jazz, Hip Hop, etc.)
- `nivel`: Nível da turma (Iniciante, Intermediário, Avançado)
- `professor`: Professor responsável (ForeignKey para User)
- `capacidade_maxima`: Número máximo de alunos
- `ativa`: Status da turma
- `descricao`: Descrição da turma
- `data_inicio` e `data_fim`: Período da turma

### 2. **Aluno**
Representa um aluno matriculado.

**Campos:**
- `usuario`: Usuário associado (OneToOne com User)
- `cpf`: CPF do aluno (único)
- `data_nascimento`: Data de nascimento
- `telefone` e `telefone_emergencia`: Contatos
- `endereco`: Endereço completo
- `turmas`: Turmas matriculadas (ManyToMany)
- `data_matricula`: Data de matrícula
- `ativo`: Status do aluno
- `observacoes`: Observações gerais
- `foto`: Foto do aluno

### 3. **HorarioAula**
Define os horários regulares das aulas.

**Campos:**
- `turma`: Turma associada
- `dia_semana`: Dia da semana (SEG, TER, QUA, etc.)
- `hora_inicio` e `hora_fim`: Horário da aula
- `sala`: Sala onde ocorre a aula

### 4. **Aula**
Representa uma aula específica realizada.

**Campos:**
- `turma`: Turma da aula
- `data`: Data da aula
- `hora_inicio` e `hora_fim`: Horário
- `tema`: Tema da aula
- `conteudo`: Conteúdo abordado
- `realizada`: Status de realização
- `observacoes`: Observações

### 5. **Frequencia**
Registra a presença dos alunos nas aulas.

**Campos:**
- `aluno`: Aluno
- `aula`: Aula
- `status`: Status (PRESENTE, FALTA, FALTA_JUSTIFICADA, ATESTADO)
- `justificativa`: Justificativa de falta
- `data_registro`: Data do registro

### 6. **Aviso**
Sistema de avisos e comunicados.

**Campos:**
- `titulo` e `conteudo`: Título e texto do aviso
- `tipo`: Tipo (GERAL, TURMA, ALUNO, EVENTO, URGENTE)
- `autor`: Criador do aviso
- `turma` e `aluno`: Destinatários específicos (opcional)
- `data_criacao` e `data_expiracao`: Período de validade
- `ativo`: Status do aviso
- `importante`: Marcador de importância

### 7. **Mensalidade**
Controle financeiro das mensalidades.

**Campos:**
- `aluno`: Aluno
- `mes_referencia`: Mês de referência
- `valor`, `valor_desconto`, `valor_final`: Valores
- `data_vencimento` e `data_pagamento`: Datas
- `status`: Status (PENDENTE, PAGO, ATRASADO, CANCELADO)
- `forma_pagamento`: Forma de pagamento
- `observacoes`: Observações

### 8. **Mensagem**
Sistema de mensagens entre usuários.

**Campos:**
- `remetente` e `destinatario`: Usuários
- `assunto` e `conteudo`: Conteúdo da mensagem
- `data_envio`: Data de envio
- `lida`: Status de leitura
- `data_leitura`: Data de leitura

## 🌐 Views (Template Views)

### Views Principais:

1. **`painel_aluno`** - Dashboard principal do aluno
2. **`horarios_aulas`** - Visualização de horários
3. **`avisos`** - Lista de avisos
4. **`minhas_aulas`** - Histórico de aulas
5. **`frequencia_aluno`** - Relatório de frequência
6. **`mensalidades_aluno`** - Histórico financeiro
7. **`comunicacao`** - Sistema de mensagens
8. **`perfil_aluno`** - Perfil do aluno

## 🔌 API REST

### Endpoints Disponíveis:

#### **Alunos**
- `GET /api/painel-aluno/alunos/` - Lista alunos
- `GET /api/painel-aluno/alunos/me/` - Dados do aluno logado
- `GET /api/painel-aluno/alunos/dashboard/` - Dados do dashboard

#### **Turmas**
- `GET /api/painel-aluno/turmas/` - Lista turmas do aluno

#### **Aulas**
- `GET /api/painel-aluno/aulas/` - Lista aulas
- `GET /api/painel-aluno/aulas/proximas/` - Próximas aulas

#### **Horários**
- `GET /api/painel-aluno/horarios/` - Lista horários

#### **Frequências**
- `GET /api/painel-aluno/frequencias/` - Lista frequências
- `GET /api/painel-aluno/frequencias/estatisticas/` - Estatísticas de frequência

#### **Avisos**
- `GET /api/painel-aluno/avisos/` - Lista avisos

#### **Mensalidades**
- `GET /api/painel-aluno/mensalidades/` - Lista mensalidades
- `GET /api/painel-aluno/mensalidades/pendentes/` - Mensalidades pendentes

#### **Mensagens**
- `GET /api/painel-aluno/mensagens/` - Lista mensagens
- `POST /api/painel-aluno/mensagens/` - Criar mensagem
- `GET /api/painel-aluno/mensagens/recebidas/` - Mensagens recebidas
- `GET /api/painel-aluno/mensagens/enviadas/` - Mensagens enviadas
- `POST /api/painel-aluno/mensagens/{id}/marcar_lida/` - Marcar como lida
- `GET /api/painel-aluno/mensagens/nao_lidas/` - Contagem de não lidas

## 🔐 Autenticação

Todas as views e endpoints da API requerem autenticação. O sistema utiliza:
- Session Authentication (para templates)
- Basic Authentication (para API)

## 🛡️ Permissões

- **Alunos**: Acesso apenas aos seus próprios dados
- **Professores/Admin**: Acesso via Django Admin

## 📊 Django Admin

Todos os modelos estão registrados no Django Admin com interfaces customizadas:
- Filtros por status, data, tipo
- Campos editáveis inline
- Organização por fieldsets
- Estatísticas e contagens

## 🚀 Como Usar

### 1. Instalar Dependências
```bash
pip install -r requirements.txt
```

### 2. Aplicar Migrações
```bash
python manage.py migrate
```

### 3. Criar Superusuário
```bash
python manage.py createsuperuser
```

### 4. Rodar o Servidor
```bash
python manage.py runserver
```

### 5. Acessar

- **Portal do Aluno**: http://localhost:8000/painel-aluno/
- **API REST**: http://localhost:8000/api/painel-aluno/
- **Admin**: http://localhost:8000/admin/

## 📝 URLs Disponíveis

### Templates:
- `/painel-aluno/` - Dashboard
- `/painel-aluno/horarios/` - Horários
- `/painel-aluno/avisos/` - Avisos
- `/painel-aluno/minhas-aulas/` - Minhas Aulas
- `/painel-aluno/frequencia/` - Frequência
- `/painel-aluno/mensalidades/` - Mensalidades
- `/painel-aluno/comunicacao/` - Mensagens
- `/painel-aluno/perfil/` - Perfil

### API:
- `/api/painel-aluno/alunos/`
- `/api/painel-aluno/turmas/`
- `/api/painel-aluno/aulas/`
- `/api/painel-aluno/horarios/`
- `/api/painel-aluno/frequencias/`
- `/api/painel-aluno/avisos/`
- `/api/painel-aluno/mensalidades/`
- `/api/painel-aluno/mensagens/`

## 🔧 Configurações Importantes

### settings.py

```python
INSTALLED_APPS = [
    ...
    'rest_framework',
    'painel_aluno_app',
    ...
]

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
}
```

## 📦 Estrutura de Arquivos

```
painel_aluno_app/
├── models.py          # Modelos de dados
├── views.py           # Views para templates
├── viewsets.py        # ViewSets para API REST
├── serializers.py     # Serializers DRF
├── urls.py            # URLs de templates
├── api_urls.py        # URLs de API
├── admin.py           # Configuração do Admin
├── migrations/        # Migrações do banco
└── templates/         # Templates HTML
```

## 🎯 Próximos Passos

1. Criar templates HTML para cada view
2. Implementar sistema de notificações em tempo real
3. Adicionar filtros e busca avançada na API
4. Implementar relatórios em PDF
5. Adicionar testes unitários
6. Implementar cache para melhor performance

## 📞 Suporte

Para dúvidas ou problemas, consulte a documentação do Django e Django REST Framework:
- https://docs.djangoproject.com/
- https://www.django-rest-framework.org/

---

**Desenvolvido para GIRO DNC** 🎭💃
