# 💰 Sistema de Despesas Pessoais dos Alunos

## 📋 Descrição

Sistema completo para os alunos gerenciarem suas **despesas pessoais** relacionadas às atividades da escola de dança. Os alunos podem criar, editar, acompanhar e organizar todos os gastos relacionados a viagens, figurinos, apresentações e muito mais!

## ✨ Funcionalidades

### Para Alunos:
- ✅ **Criar despesas personalizadas** (ex: "Viagem São Paulo - Agosto/2025")
- ✅ **Categorizar gastos** (Figurino, Viagem, Apresentação, Maquiagem, etc.)
- ✅ **Acompanhar orçamento** (valor previsto vs valor gasto)
- ✅ **Visualizar estatísticas** em cards e gráficos
- ✅ **Filtrar por mês, categoria e status**
- ✅ **Editar e excluir despesas**
- ✅ **Adicionar detalhes** (itens, observações, parcelamentos)
- ✅ **Relacionar com turmas** (opcional)

### Para Administradores:
- ✅ **Visualizar todas as despesas** no Django Admin
- ✅ **Filtros avançados** por aluno, categoria, status, data
- ✅ **Badges coloridos** para categorias e status
- ✅ **Análise de percentuais** e valores

## 🎯 Casos de Uso Reais

### Exemplo 1: Viagem para Competição
```
Nome: Viagem Campeonato Nacional - São Paulo
Categoria: Viagem
Valor Previsto: R$ 1.500,00
Status: Planejado
Data Prevista: 15/08/2025

Itens:
- Passagem de ônibus: R$ 200,00
- Hospedagem (3 diárias): R$ 600,00
- Alimentação: R$ 300,00
- Taxa de inscrição: R$ 400,00

Observações: Parcelado em 3x no cartão
```

### Exemplo 2: Figurino para Apresentação
```
Nome: Figurino Apresentação de Natal 2025
Categoria: Figurino
Valor Previsto: R$ 800,00
Valor Gasto: R$ 350,00
Status: Parcial
Data Prevista: 20/12/2025

Itens:
- Vestido: R$ 250,00 ✓ PAGO
- Sapato: R$ 150,00 ✓ PAGO
- Acessórios: R$ 100,00 (FALTA)
- Maquiagem: R$ 150,00 (FALTA)
- Penteado: R$ 150,00 (FALTA)

Observações: Já comprei vestido e sapato. Falta maquiagem e acessórios para dezembro.
```

### Exemplo 3: Despesas Mensais
```
Nome: Despesas Agosto - Apresentações
Categoria: Apresentacao
Valor Previsto: R$ 500,00
Valor Gasto: R$ 520,00
Status: Pago
Data Prevista: 31/08/2025

Observações: ⚠ Estouro de R$ 20,00 - próximo mês ajustar orçamento
```

## 🗂️ Categorias Disponíveis

| Categoria | Descrição | Exemplos |
|-----------|-----------|----------|
| **FIGURINO** | Roupas para apresentações | Vestidos, fantasias, uniformes |
| **VIAGEM** | Viagens e excursões | Passagens, hospedagem, traslados |
| **APRESENTACAO** | Custos de eventos | Taxa de inscrição, certificados |
| **ACESSORIO** | Acessórios e complementos | Bijuterias, tiaras, faixas |
| **TRANSPORTE** | Locomoção | Uber, táxi, combustível |
| **ALIMENTACAO** | Alimentação em eventos | Refeições, lanches, água |
| **HOSPEDAGEM** | Estadias | Hotel, pousada, Airbnb |
| **MAQUIAGEM** | Maquiagem e produtos | Base, sombra, batom, removedor |
| **CABELO** | Cabelo e penteados | Salão, grampos, spray fixador |
| **SAPATO** | Calçados | Sapatilhas, sapatos de salto |
| **OUTRO** | Outras despesas | Diversos |

## 📊 Status de Despesas

| Status | Cor | Significado |
|--------|-----|-------------|
| **PLANEJADO** | 🟠 Laranja | Despesa futura, ainda não paga |
| **PAGO** | 🟢 Verde | Totalmente quitada |
| **PARCIAL** | 🟡 Amarelo | Parcialmente paga |
| **CANCELADO** | ⚫ Cinza | Despesa cancelada/não realizada |

## 🎨 Interface do Usuário

### Dashboard Principal (`/minhas-despesas/`)

#### 📈 Cards de Resumo:
1. **Total Previsto** - Soma de todos os valores previstos
2. **Total Gasto** - Soma de todos os valores já gastos
3. **Restante/Estouro** - Diferença (verde se positivo, vermelho se negativo)

#### 📊 Gráfico de Pizza:
- Visualização de gastos por categoria
- Cores vibrantes para cada categoria
- Valores em R$ no tooltip

#### 🔍 Filtros:
- **Por Mês**: Selecionar mês/ano específico
- **Por Categoria**: Filtrar por tipo de despesa
- **Por Status**: Planejado, Pago, Parcial, Cancelado

#### 📋 Lista de Despesas:
- Cards com todas as informações
- Barra de progresso visual
- Menu de ações (Editar/Excluir)
- Badges coloridos

### Formulário de Criação (`/minhas-despesas/criar/`)

#### Campos Obrigatórios:
- Nome da Despesa
- Descrição
- Categoria
- Valor Previsto
- Data Prevista
- Status

#### Campos Opcionais:
- Turma Relacionada
- Valor Já Gasto
- Data de Pagamento
- Itens (lista detalhada)
- Observações

### Formulário de Edição (`/minhas-despesas/editar/<id>/`)

- Todos os campos do formulário de criação
- **NOVO**: Painel de Status Atual mostrando:
  - Valor Restante (colorido)
  - Percentual Gasto
  - Situação do Orçamento
- **NOVO**: Validação visual em tempo real
- **NOVO**: Informações de auditoria (criação/atualização)
- Botão de Excluir Despesa

## 🛠️ Aspectos Técnicos

### Models
```python
class DespesaAluno(models.Model):
    aluno = ForeignKey(Aluno)
    nome = CharField(max_length=200)
    descricao = CharField(max_length=300)
    categoria = CharField(choices=CATEGORIA_CHOICES)
    turma = ForeignKey(Turma, null=True, blank=True)
    valor_previsto = DecimalField(max_digits=10, decimal_places=2)
    valor_gasto = DecimalField(max_digits=10, decimal_places=2)
    status = CharField(choices=STATUS_CHOICES)
    data_prevista = DateField()
    data_pagamento = DateField(null=True, blank=True)
    observacoes = TextField(blank=True)
    itens = TextField(blank=True)
    
    # Methods
    def valor_restante()
    def percentual_gasto()
    def esta_dentro_orcamento()
    def diferenca_orcamento()
```

### URLs
```python
path('minhas-despesas/', views.minhas_despesas, name='minhas_despesas')
path('minhas-despesas/criar/', views.criar_despesa, name='criar_despesa')
path('minhas-despesas/editar/<int:despesa_id>/', views.editar_despesa, name='editar_despesa')
path('minhas-despesas/deletar/<int:despesa_id>/', views.deletar_despesa, name='deletar_despesa')
```

### Views
- `minhas_despesas()` - Dashboard com listagem e filtros
- `criar_despesa()` - Criação de nova despesa
- `editar_despesa()` - Edição de despesa existente
- `deletar_despesa()` - Exclusão (POST only)

### Admin
```python
@admin.register(DespesaAluno)
class DespesaAlunoAdmin(admin.ModelAdmin):
    list_display = [
        'aluno', 'nome', 'categoria_badge', 'data_prevista',
        'valor_previsto_display', 'valor_gasto_display',
        'percentual_display', 'status_badge'
    ]
    list_filter = ['status', 'categoria', 'data_prevista', 'turma']
    search_fields = ['aluno__usuario__first_name', 'nome', 'descricao']
```

## 🎯 Benefícios para os Alunos

### 📊 Organização Financeira:
- ✅ Planejar gastos com antecedência
- ✅ Acompanhar orçamento em tempo real
- ✅ Evitar surpresas financeiras
- ✅ Ter histórico completo de despesas

### 💡 Consciência Financeira:
- ✅ Visualizar onde o dinheiro está sendo gasto
- ✅ Identificar categorias com mais gastos
- ✅ Aprender a fazer orçamentos
- ✅ Controlar estouros de orçamento

### 🎯 Praticidade:
- ✅ Tudo em um só lugar
- ✅ Acesso de qualquer dispositivo
- ✅ Informações sempre atualizadas
- ✅ Fácil de usar e entender

## 📱 Responsividade

- ✅ **Mobile First** - Funciona perfeitamente em smartphones
- ✅ **Tablet** - Layout adaptado para tablets
- ✅ **Desktop** - Melhor experiência em telas grandes

## 🔒 Segurança

- ✅ **@login_required** - Apenas usuários autenticados
- ✅ **Isolamento de dados** - Cada aluno vê apenas suas despesas
- ✅ **Validação no servidor** - Proteção contra dados inválidos
- ✅ **CSRF Protection** - Proteção contra ataques CSRF

## 🚀 Como Usar

### Para Alunos:

1. **Acesse o menu** "Minhas Despesas"

2. **Crie sua primeira despesa:**
   - Clique em "Nova Despesa"
   - Preencha o nome (ex: "Viagem Agosto")
   - Escolha a categoria
   - Defina valor previsto
   - Salve!

3. **Acompanhe seus gastos:**
   - Conforme for gastando, edite a despesa
   - Atualize o "Valor Gasto"
   - Veja o percentual e barra de progresso

4. **Use os filtros:**
   - Filtre por mês para ver despesas específicas
   - Filtre por categoria para análises
   - Filtre por status para organizar

5. **Analise os gráficos:**
   - Veja quais categorias gastam mais
   - Identifique oportunidades de economia

### Para Administradores:

1. **Acesse o Django Admin**
2. **Vá em "Despesas dos Alunos"**
3. **Use filtros para análises:**
   - Por aluno
   - Por categoria
   - Por período
   - Por status

## 🎨 Cores e Identidade Visual

### Categorias:
- **Figurino**: Rosa (`#ec4899`)
- **Viagem**: Azul (`#3b82f6`)
- **Apresentação**: Roxo (`#8b5cf6`)
- **Acessório**: Amarelo (`#f59e0b`)
- **Transporte**: Verde (`#10b981`)
- **Alimentação**: Vermelho (`#ef4444`)
- **Hospedagem**: Indigo (`#6366f1`)
- **Maquiagem**: Rosa (`#ec4899`)
- **Cabelo**: Laranja (`#f97316`)
- **Sapato**: Roxo (`#8b5cf6`)

### Status:
- **Planejado**: Laranja (`#f97316`)
- **Pago**: Verde (`#22c55e`)
- **Parcial**: Amarelo (`#eab308`)
- **Cancelado**: Cinza (`#6b7280`)

## 📝 Exemplos de Fluxo

### Fluxo 1: Planejamento de Viagem
```
1. Aluno é avisado: "Viagem em Agosto"
2. Cria despesa: "Viagem SP - Agosto/2025"
3. Define valor previsto: R$ 1.500,00
4. Status: PLANEJADO
5. Adiciona itens detalhados
6. Conforme vai comprando:
   - Atualiza valor gasto
   - Vê progresso na barra
   - Controla orçamento
7. Quando terminar:
   - Status: PAGO
   - Compara previsto vs real
```

### Fluxo 2: Preparação para Apresentação
```
1. Apresentação marcada para Dezembro
2. Cria: "Figurino Natal 2025"
3. Lista todos os itens necessários
4. Valor previsto: R$ 800,00
5. Compra por etapas:
   - Semana 1: Vestido (R$ 250)
   - Semana 2: Sapato (R$ 150)
   - Semana 3: Acessórios e maquiagem
6. Acompanha percentual gasto
7. Evita estouro de orçamento
```

## 🎓 Dicas de Uso

### Para Melhor Organização:
1. **Crie despesas assim que souber** do evento/necessidade
2. **Use nomes descritivos** que facilitem identificação
3. **Atualize regularmente** o valor gasto
4. **Use o campo "Itens"** para detalhar componentes
5. **Aproveite as observações** para lembretes
6. **Relacione com turmas** quando aplicável
7. **Revise mensalmente** seus gastos

### Para Economizar:
1. **Compare previsto vs gasto** regularmente
2. **Identifique categorias** com mais gastos
3. **Planeje com antecedência** para melhores preços
4. **Use os filtros** para análises mensais
5. **Compartilhe custos** quando possível

## 🔄 Atualizações Futuras (Ideias)

- 📸 Upload de fotos de comprovantes
- 📊 Relatórios em PDF
- 📧 Alertas por email de despesas próximas
- 👥 Compartilhamento de despesas entre alunos
- 💳 Integração com meios de pagamento
- 📈 Gráficos de evolução temporal
- 🏆 Metas de economia
- 📱 App mobile nativo

## ✅ Checklist de Implementação

- [x] Model `DespesaAluno` criado
- [x] Admin interface com badges coloridos
- [x] View `minhas_despesas` com dashboard
- [x] View `criar_despesa` com formulário
- [x] View `editar_despesa` com validações
- [x] View `deletar_despesa` com confirmação
- [x] Template dashboard com gráficos Chart.js
- [x] Template criação com hints
- [x] Template edição com cálculos em tempo real
- [x] URLs configuradas
- [x] Migration aplicada
- [x] Documentação completa

## 📞 Suporte

Em caso de dúvidas ou problemas:
- Verifique se está logado como aluno
- Confira se a migration foi aplicada
- Verifique permissões de usuário
- Consulte o Django Admin para debug

---

**Sistema criado com ❤️ para os alunos da Giro Dance!**
