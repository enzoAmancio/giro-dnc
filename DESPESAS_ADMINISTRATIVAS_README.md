# 💼 Sistema de Gestão de Despesas Administrativas - Giro DNC

## 📝 Visão Geral

Sistema completo e interativo para gerenciar despesas administrativas da Giro DNC, incluindo:
- Aluguel, contas (luz, água, internet)
- Salários e encargos
- Equipamentos e manutenção
- Marketing e publicidade
- Impostos e taxas
- E muito mais!

---

## 🎯 Funcionalidades Implementadas

### ✅ Model Completo (DespesaAdministrativa)

**Categorias Disponíveis:**
- Aluguel, Energia Elétrica, Água
- Internet/Telefone, Salários
- Equipamentos, Manutenção, Limpeza
- Material de Consumo, Marketing/Publicidade
- Impostos/Taxas, Seguros
- Transporte/Combustível, Alimentação
- Eventos/Apresentações, Software/Licenças
- Jurídico/Contábil, Outros

**Campos Principais:**
- `nome`: Nome descritivo da despesa
- `categoria`: Categoria da despesa (18 opções)
- `fornecedor`: Empresa ou pessoa que receberá o pagamento
- `valor_total`: Valor total da despesa
- `valor_pago`: Quanto já foi pago
- `data_vencimento`: Data limite para pagamento
- `data_pagamento`: Quando foi efetivamente pago
- `status`: PENDENTE, PAGO, ATRASADO, PARCIAL, CANCELADO
- `tipo_pagamento`: FIXO, VARIÁVEL, ÚNICO, PARCELADO
- `forma_pagamento`: Dinheiro, Débito, Crédito, PIX, etc.
- `numero_parcelas` e `parcela_atual`: Para despesas parceladas
- `comprovante`: Upload de arquivos PDF/JPG/PNG
- `observacoes`: Anotações adicionais

**Métodos Úteis:**
- `valor_pendente()`: Calcula quanto falta pagar
- `percentual_pago()`: Percentual já pago
- `esta_pago()`: Verifica se está totalmente pago
- `esta_atrasado()`: Verifica se está atrasado
- `dias_ate_vencimento()`: Dias até o vencimento
- `get_categoria_color()`: Cor da categoria
- `get_status_color()`: Cor do status

---

### ✅ Views (paginas/views.py)

#### 1. **despesas_administrativas(request)**
**URL:** `/despesas-admin/`  
**Acesso:** Apenas staff (@staff_member_required)

**Funcionalidades:**
- Dashboard interativo com cards de resumo
- Filtros avançados (mês, categoria, status, tipo)
- Estatísticas gerais:
  - Total de despesas
  - Total pago
  - Total pendente
  - Despesas atrasadas
- Gráfico de categorias (Barras)
- Gráfico de status (Doughnut)
- Alerta de despesas vencendo nos próximos 7 dias
- Top 5 maiores despesas
- Tabela completa e responsiva
- Exportação para Excel

#### 2. **criar_despesa_admin(request)**
**URL:** `/despesas-admin/criar/`  
**Acesso:** Apenas staff

**Funcionalidades:**
- Formulário completo para criar nova despesa
- Upload de comprovante
- Validação de campos obrigatórios
- Registro automático do usuário criador

#### 3. **editar_despesa_admin(request, despesa_id)**
**URL:** `/despesas-admin/editar/<id>/`  
**Acesso:** Apenas staff

**Funcionalidades:**
- Edição de despesa existente
- Formulário pré-preenchido
- Atualização de comprovante (opcional)

#### 4. **deletar_despesa_admin(request, despesa_id)**
**URL:** `/despesas-admin/deletar/<id>/`  
**Acesso:** Apenas staff (POST only)

**Funcionalidades:**
- Exclusão segura com confirmação
- Mensagem de sucesso

#### 5. **exportar_despesas_admin_excel(request)**
**URL:** `/despesas-admin/exportar/`  
**Acesso:** Apenas staff

**Funcionalidades:**
- Exporta para Excel (.xlsx)
- Inclui todos os dados importantes
- Respeita filtros aplicados
- Formatação profissional com cores e estilos

---

### ✅ Templates

#### 1. **despesas_administrativas.html**
Dashboard principal com:
- **Header:** Breadcrumb, título, botões de ação
- **Alerta:** Despesas vencendo em 7 dias
- **Cards de Resumo (4):**
  - Total de Despesas
  - Total Pago
  - Total Pendente
  - Em Atraso
- **Filtros Avançados:**
  - Mês, Categoria, Status, Tipo
  - Design gradiente moderno
- **Gráficos Interativos (Chart.js):**
  - Despesas por Categoria (Barras coloridas)
  - Status das Despesas (Doughnut)
- **Top 5 Maiores Despesas**
- **Tabela Completa:**
  - Badges coloridos por categoria e status
  - Progress bar de pagamento
  - Indicadores de atraso
  - Ações (Editar/Excluir)
- **Modal de Confirmação de Exclusão**

#### 2. **criar_despesa_admin.html**
Formulário de criação com:
- Layout em grid responsivo
- Campos agrupados logicamente
- Upload de arquivo
- Validação HTML5

#### 3. **editar_despesa_admin.html**
Formulário de edição com:
- Valores pré-preenchidos
- Link para comprovante existente
- Mesma estrutura do formulário de criação

---

### ✅ Admin Django (paginas/admin.py)

**DespesaAdministrativaAdmin:**
- **Lista:** Nome, categoria (badge), fornecedor, valores, status (badge)
- **Filtros:** Status, categoria, tipo, forma de pagamento, datas
- **Busca:** Nome, descrição, fornecedor, documento, observações
- **Hierarquia:** Por data de vencimento
- **Campos Read-Only:** Criado por, datas de criação/atualização, campos calculados
- **Fieldsets Organizados:**
  - Informações Básicas
  - Fornecedor
  - Valores
  - Datas
  - Status e Pagamento
  - Parcelamento (colapsável)
  - Documentação
  - Metadados (colapsável)
- **Métodos Customizados:**
  - `categoria_badge()`: Badge colorido
  - `status_badge()`: Badge colorido
  - `valor_total_display()`: Formatado
  - `valor_pago_display()`: Formatado
  - `valor_pendente_display()`: Formatado com cor dinâmica

---

### ✅ URLs (paginas/urls.py)

```python
path('despesas-admin/', views.despesas_administrativas, name='despesas_administrativas'),
path('despesas-admin/criar/', views.criar_despesa_admin, name='criar_despesa_admin'),
path('despesas-admin/editar/<int:despesa_id>/', views.editar_despesa_admin, name='editar_despesa_admin'),
path('despesas-admin/deletar/<int:despesa_id>/', views.deletar_despesa_admin, name='deletar_despesa_admin'),
path('despesas-admin/exportar/', views.exportar_despesas_admin_excel, name='exportar_despesas_admin_excel'),
```

---

### ✅ Sidebar Atualizado

Adicionado no menu **Administração** (apenas para superuser):
```html
<a href="{% url 'paginas:despesas_administrativas' %}" class="nav-link sidebar-option">
  <i class="bi bi-wallet2"></i>
  <span>Despesas Admin</span>
</a>
```

---

## 🎨 Design & UX

### Características Visuais:
- **Cards de Resumo:** Gradientes modernos, ícones grandes, animações hover
- **Filtros:** Seção com gradiente roxo, campos brancos com sombra
- **Gráficos:** Chart.js com cores dinâmicas e responsivos
- **Tabela:** Badges coloridos, progress bars, indicadores visuais
- **Botões:** Bootstrap 5 com ícones Bootstrap Icons
- **Responsivo:** Mobile-first, funciona em todos os dispositivos

### Cores do Sistema:
- **Verde (#22c55e):** Pago, positivo
- **Laranja (#f59e0b):** Pendente, atenção
- **Vermelho (#ef4444):** Atrasado, negativo
- **Azul (#3b82f6):** Parcial, informação
- **Cinza (#6b7280):** Cancelado, neutro

---

## 📊 Gráficos Interativos

### 1. Gráfico de Categorias (Barras)
- Mostra valor total por categoria
- Cores dinâmicas baseadas em HSL
- Tooltips formatados em R$
- Responsivo

### 2. Gráfico de Status (Doughnut)
- Distribuição: Pagas, Pendentes, Atrasadas
- Cores fixas (verde, laranja, vermelho)
- Legenda na parte inferior
- Valores em R$

---

## 🔐 Segurança

- Acesso restrito a staff (`@staff_member_required`)
- CSRF Protection em todos os formulários
- Validação de dados no backend
- Upload de arquivos com restrição de formato
- Registro de quem criou cada despesa
- Timestamps automáticos

---

## 📦 Dependências

- Django (já instalado)
- openpyxl (para exportação Excel)
- Bootstrap 5.3.3
- Bootstrap Icons 1.11.3
- Chart.js 4.4.0

---

## 🚀 Como Usar

### 1. Acessar o Sistema
```
http://127.0.0.1:8000/despesas-admin/
```

### 2. Criar Nova Despesa
1. Clique em "Nova Despesa"
2. Preencha os campos obrigatórios (*, nome, categoria, valor total, status, tipo)
3. Adicione informações opcionais (fornecedor, comprovante, etc.)
4. Clique em "Salvar Despesa"

### 3. Filtrar Despesas
1. Use os filtros no topo (mês, categoria, status, tipo)
2. Clique em "Filtrar"
3. Para limpar, clique no ícone X

### 4. Visualizar Estatísticas
- Cards de resumo mostram totais em tempo real
- Gráficos atualizam automaticamente com os filtros
- Top 5 maiores despesas sempre visível

### 5. Exportar para Excel
1. Aplique filtros desejados (opcional)
2. Clique em "Exportar"
3. Arquivo .xlsx será baixado

### 6. Editar/Excluir
- **Editar:** Clique no ícone lápis na tabela
- **Excluir:** Clique no ícone lixeira → Confirme no modal

---

## 📱 Responsividade

O sistema é 100% responsivo:
- **Desktop:** Layout completo com gráficos lado a lado
- **Tablet:** Cards em 2 colunas, gráficos empilhados
- **Mobile:** Cards e gráficos empilhados, tabela com scroll horizontal

---

## 🎯 Próximos Passos (Opcional)

1. **Dashboard de Analytics:**
   - Gráfico de linha com evolução mensal
   - Comparação ano a ano
   - Previsões baseadas em histórico

2. **Notificações:**
   - Email automático para despesas vencendo
   - Alertas no sistema

3. **Relatórios Avançados:**
   - PDF customizado
   - Múltiplos gráficos
   - Análise de tendências

4. **Integração Bancária:**
   - Import de OFX
   - Reconciliação automática

5. **Orçamento:**
   - Definir orçamento mensal por categoria
   - Comparar previsto vs realizado

---

## ✨ Conclusão

Sistema completo e profissional de gestão de despesas administrativas, totalmente integrado ao ecossistema Giro DNC, com:
- ✅ Interface moderna e intuitiva
- ✅ Gráficos interativos
- ✅ Filtros avançados
- ✅ Exportação para Excel
- ✅ Controle de acesso
- ✅ Design responsivo
- ✅ Código limpo e documentado

**Pronto para uso em produção!** 🚀
