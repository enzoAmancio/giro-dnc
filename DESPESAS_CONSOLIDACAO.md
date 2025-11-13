# Consolidação do Sistema de Despesas

## Objetivo
Unificar o acesso às despesas em uma única URL (`/financeiro/despesas/`) que exibe conteúdo diferente baseado no tipo de usuário.

## Alterações Implementadas

### 1. View Unificada (`paginas/views.py`)

A função `financeiro_despesas()` foi modificada para detectar o tipo de usuário:

```python
@login_required
def financeiro_despesas(request):
    """Exibir despesas - Admin vê gestão ou Students veem despesas pessoais"""
    
    # Se for staff (admin/professor), mostrar view administrativa
    if request.user.is_staff:
        context = {
            'usuario': request.user,
            'is_admin_view': True,
        }
        return render(request, 'financeiro/despesas.html', context)
    
    # Se for aluno, mostrar sistema de despesas pessoais
    try:
        aluno = Aluno.objects.get(usuario=request.user)
    except Aluno.DoesNotExist:
        messages.error(request, 'Você precisa estar cadastrado como aluno.')
        return redirect('paginas:painel_aluno')
    
    # [Lógica de filtros e estatísticas para alunos...]
```

**Comportamento:**
- **Staff (is_staff=True)**: Vê a interface administrativa de resultados financeiros mensais
- **Alunos**: Veem seu dashboard pessoal de despesas (viagens, figurinos, etc.)

### 2. Template Condicional (`financeiro/despesas.html`)

O template foi atualizado com blocos condicionais:

```django
{% if is_admin_view %}
    {# ========== ADMIN VIEW - Resultados Financeiros Mensais ========== #}
    <!-- Conteúdo administrativo -->
    
{% else %}
    {# ========== STUDENT VIEW - Despesas Pessoais do Aluno ========== #}
    <!-- Dashboard de despesas pessoais -->
    
{% endif %}
```

**Funcionalidades da View de Aluno:**
- Cards de resumo (Total Previsto, Total Gasto, Restante/Estouro)
- Gráfico de pizza com gastos por categoria (Chart.js)
- Filtros por mês, categoria e status
- Tabela com todas as despesas
- Botão "Nova Despesa" para criar registros
- Links para editar despesas existentes

### 3. Métodos de Cor no Model (`paginas/models.py`)

Adicionados métodos ao `DespesaAluno` para exibir badges coloridos:

```python
def get_categoria_color(self):
    """Retorna a cor apropriada para cada categoria"""
    cores = {
        'FIGURINO': '#3b82f6',      # Azul
        'VIAGEM': '#ef4444',        # Vermelho
        'APRESENTACAO': '#22c55e',  # Verde
        'ACESSORIO': '#f59e0b',     # Âmbar
        'TRANSPORTE': '#8b5cf6',    # Roxo
        'ALIMENTACAO': '#ec4899',   # Pink
        'HOSPEDAGEM': '#14b8a6',    # Teal
        'MAQUIAGEM': '#f97316',     # Laranja
        'CABELO': '#6366f1',        # Indigo
        'SAPATO': '#84cc16',        # Lima
        'OUTRO': '#6b7280',         # Cinza
    }
    return cores.get(self.categoria, '#6b7280')

def get_status_color(self):
    """Retorna a cor apropriada para o status"""
    return self.status_cor()
```

## URLs do Sistema

### Visualização Principal
- `/financeiro/despesas/` → View unificada (admin OU aluno)

### Ações de Aluno (CRUD)
- `/minhas-despesas/criar/` → Criar nova despesa
- `/minhas-despesas/editar/<id>/` → Editar despesa existente
- `/minhas-despesas/deletar/<id>/` → Deletar despesa

### URLs Administrativas
- `/financeiro/resultados-mensais/` → Resultados financeiros mensais (admin)
- `/financeiro/resultados-mensais/exportar/` → Exportar Excel (admin)

## Benefícios

1. **UX Simplificada**: Um único ponto de acesso para "Despesas" no menu
2. **Segurança**: Controle automático de acesso baseado em `is_staff`
3. **Manutenibilidade**: Lógica centralizada em uma view
4. **Escalabilidade**: Fácil adicionar novos tipos de usuário no futuro

## Como Testar

### Como Administrador
1. Login com usuário staff
2. Acesse `/financeiro/despesas/`
3. Deve ver: Resultados Financeiros Mensais

### Como Aluno
1. Login com usuário aluno (não-staff)
2. Acesse `/financeiro/despesas/`
3. Deve ver: Dashboard de Despesas Pessoais com:
   - Cards de resumo financeiro
   - Gráfico de gastos por categoria
   - Filtros (mês, categoria, status)
   - Lista de despesas com badges coloridos
   - Botão "Nova Despesa"

## Notas Técnicas

- **Filtros**: Funcionam via query parameters GET (`?mes=2025-03&categoria=VIAGEM`)
- **Gráfico**: Usa Chart.js (doughnut) com cores dinâmicas
- **Badges**: Cores definidas nos métodos do model para consistência
- **Responsividade**: Layout Bootstrap 5.3.3 totalmente responsivo
- **Ícones**: Bootstrap Icons 1.11.3

## Arquivos Modificados

1. `paginas/views.py` - View `financeiro_despesas()`
2. `paginas/models.py` - Métodos `get_categoria_color()` e `get_status_color()`
3. `paginas/templates/financeiro/despesas.html` - Template condicional
4. `paginas/urls.py` - URLs já configuradas (sem alterações)

## Status

✅ **CONCLUÍDO E PRONTO PARA PRODUÇÃO**

- View unificada implementada
- Template com blocos condicionais
- Métodos de cor adicionados ao model
- Static files coletados
- Testes recomendados antes de deploy
