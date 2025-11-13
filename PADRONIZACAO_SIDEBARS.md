# Padronização de Sidebars - Giro DNC

## ✅ Problema Resolvido

**Situação anterior:** Cada template tinha seu próprio sidebar inline com diferenças:
- Alguns tinham botão "Sair", outros não
- Alguns colapsavam corretamente, outros não
- Menus em diferentes posições
- Código duplicado e difícil de manter

**Solução implementada:** Sidebars centralizados e reutilizáveis com variáveis de contexto.

---

## 📁 Arquivos Criados

### 1. `paginas/templates/includes/sidebar.html`
**Propósito:** Sidebar padrão para templates com estrutura `<div class="gd-layout">`

**Usado em:**
- Todos os templates de `painel/`
- Todos os templates de `financeiro/` (exceto despesas pessoais)
- Todos os templates de `eventos/`
- Todos os templates de `admin_painel/`

**Variáveis de contexto necessárias:**
```django
{% with sidebar_section='financeiro' sidebar_active='financeiro_mensalidades' %}
  {% include 'includes/sidebar.html' %}
{% endwith %}
```

### 2. `paginas/templates/painel/sidebar.html`
**Propósito:** Sidebar para templates com estrutura `container-fluid + row`

**Usado em:**
- `financeiro/minhas_despesas.html`
- `financeiro/criar_despesa.html`
- `financeiro/editar_despesa.html`

**Variáveis de contexto necessárias:**
```django
{% with sidebar_section='financeiro' sidebar_active='financeiro_despesas' %}
  {% include 'painel/sidebar.html' %}
{% endwith %}
```

---

## 🎯 Estrutura do Sidebar Padronizado

### Seções (sidebar_section)
- `painel` - Painel do Aluno
- `financeiro` - Financeiro
- `eventos` - Eventos
- `aulas` - Minhas Aulas
- `comunicacao` - Comunicação
- `admin` - Administração (apenas superuser)

### Páginas Ativas (sidebar_active)
**Painel:**
- `painel_index`
- `painel_horarios`
- `painel_avisos`

**Financeiro:**
- `financeiro_mensalidades`
- `financeiro_extrato`
- `financeiro_despesas`

**Eventos:**
- `eventos_lista`
- `minhas_vendas`

**Aulas:**
- `painel_minhas_aulas`

**Comunicação:**
- `painel_comunicacao`
- `painel_chat`

**Admin:**
- `admin_dashboard`
- `admin_alunos`
- `admin_turmas`
- `admin_aulas`
- `admin_frequencia`
- `admin_mensalidades`
- `admin_eventos`
- `admin_avisos`

---

## 📊 Templates Atualizados

### ✅ Atualizados Automaticamente (18)

**Painel:**
1. `painel/index.html`
2. `painel/avisos.html`
3. `painel/minhas_aulas.html`
4. `painel/comunicacao.html`
5. `painel/chat.html`

**Financeiro:**
6. `financeiro/mensalidades.html`
7. `financeiro/Extrato.html`
8. `financeiro/despesas.html`

**Eventos:**
9. `eventos/lista.html`
10. `eventos/detalhes.html`
11. `eventos/minhas_vendas.html`

**Admin:**
12. `admin_painel/dashboard.html`
13. `admin_painel/alunos.html`
14. `admin_painel/turmas.html`
15. `admin_painel/aulas.html`
16. `admin_painel/mensalidades.html`
17. `admin_painel/eventos.html`
18. `admin_painel/avisos.html`

### ✅ Atualizados Manualmente (3)

19. `financeiro/minhas_despesas.html`
20. `financeiro/criar_despesa.html`
21. `financeiro/editar_despesa.html`

### ⚠️ Arquivos Não Encontrados (4)

- `painel/horarios.html` - Nome correto pode ser diferente
- `admin_painel/frequencia.html` - Pode não existir ainda
- `admin_painel/detalhes_aluno.html` - Pode não existir ainda
- `admin_painel/editar_aluno.html` - Pode não existir ainda

---

## 🎨 Funcionalidades do Sidebar Padronizado

### 1. **Botão Sair Fixo**
Todos os sidebars agora têm o botão "Sair" fixo no rodapé:
```html
<div class="gd-sidebar-footer">
  <a href="{% url 'login:logout' %}" class="nav-link sidebar-option btn-sair">
    <i class="bi bi-box-arrow-right"></i>
    <span>Sair</span>
  </a>
</div>
```

### 2. **Seções Expansíveis**
Cada seção abre/fecha com accordion do Bootstrap:
- Seção ativa (`sidebar_section`) vem aberta por padrão
- Outras seções vêm fechadas
- Apenas uma seção aberta por vez

### 3. **Item Ativo Destacado**
O item atual (`sidebar_active`) recebe a classe `active`:
```html
<a href="..." class="nav-link sidebar-option active">
```

### 4. **Visibilidade Condicional**
Seção de Administração só aparece para superusers:
```django
{% if user.is_superuser %}
  <!-- Menu Admin -->
{% endif %}
```

### 5. **Ícones Personalizados**
- Bootstrap Icons para ações comuns
- Imagens PNG para Mensalidades, Extrato e Despesas

---

## 🔧 Como Usar em Novos Templates

### Para templates com `<div class="gd-layout">`:

```django
<!DOCTYPE html>
<html>
<head>
  <!-- ... -->
  <link rel="stylesheet" href="{% static 'paginas/css/style.css' %}">
</head>
<body>
  <header class="gd-topbar">
    <!-- Logo e título -->
  </header>

  <!-- Menu Sanduíche -->
  <div class="sidebar-item">
    <button id="sidebar-toggle" class="menu-sanduiche">
      <i class="bi bi-list"></i>
    </button>
  </div>

  <div class="gd-layout d-flex">
    {% with sidebar_section='SEÇÃO' sidebar_active='PÁGINA_ATIVA' %}
      {% include 'includes/sidebar.html' %}
    {% endwith %}

    <main class="gd-main">
      <!-- Conteúdo -->
    </main>
  </div>

  <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"></script>
  <script src="{% static 'paginas/js/script.js' %}"></script>
</body>
</html>
```

### Para templates com `container-fluid`:

```django
<!DOCTYPE html>
<html>
<head>
  <!-- ... -->
</head>
<body>
  <header class="gd-topbar">
    <!-- Logo e título -->
  </header>

  <div class="sidebar-item">
    <button id="sidebar-toggle" class="menu-sanduiche">
      <i class="bi bi-list"></i>
    </button>
  </div>

  <div class="container-fluid">
    <div class="row">
      {% with sidebar_section='SEÇÃO' sidebar_active='PÁGINA_ATIVA' %}
        {% include 'painel/sidebar.html' %}
      {% endwith %}

      <main class="col-md-9 ms-sm-auto col-lg-10 px-md-4">
        <!-- Conteúdo -->
      </main>
    </div>
  </div>

  <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"></script>
  <script src="{% static 'paginas/js/script.js' %}"></script>
</body>
</html>
```

---

## 🎯 Benefícios

1. **Manutenção Centralizada:** Alterar o menu = editar 1 arquivo
2. **Consistência:** Todos os templates têm o mesmo comportamento
3. **Botão Sair:** Presente em TODAS as páginas
4. **Navegação Intuitiva:** Seção ativa sempre expandida
5. **Responsividade:** Funciona em desktop e mobile
6. **Código Limpo:** Menos duplicação de código

---

## 🧪 Testado

- ✅ Desktop (>1024px): Menu lateral colapsável
- ✅ Mobile (≤1024px): Menu overlay com botão sanduíche
- ✅ Botão "Sair" funcional em todas as páginas
- ✅ Seções expandem/colapsam corretamente
- ✅ Item ativo destacado
- ✅ Permissões (admin menu só para superuser)

---

## 📝 Notas Importantes

1. **script.js obrigatório:** Controla o comportamento do menu sanduíche
2. **style.css obrigatório:** Estilos do sidebar e responsividade
3. **Bootstrap 5.3.3:** Necessário para accordion e collapse
4. **Bootstrap Icons:** Necessário para ícones

---

**Status:** ✅ CONCLUÍDO - 21 templates padronizados
**Data:** 12 de Novembro de 2025
