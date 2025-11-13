# 📊 Sistema de Gestão Financeira Mensal - Giro DNC

## 📝 Visão Geral

Sistema completo para gerenciar e visualizar os resultados financeiros mensais da Giro DNC, permitindo ao administrador acompanhar lucros, gastos e valores a receber mês a mês.

---

## 🎯 Funcionalidades Implementadas

### ✅ Model (paginas/models.py)
- **ResultadoFinanceiroMensal**: Armazena dados financeiros mensais
  - `mes`: Data do mês de referência (único por mês)
  - `lucro_total`: Total de receitas/lucros
  - `gasto_total`: Total de despesas/gastos  
  - `a_receber_total`: Valores pendentes a receber
  - `observacoes`: Anotações opcionais
  - `data_criacao` e `data_atualizacao`: Metadados automáticos
  - `criado_por`: Usuário que criou o registro

**Métodos Calculados:**
- `lucro_liquido()`: Calcula lucro total - gasto total
- `percentual_gastos()`: % de gastos sobre o lucro
- `percentual_a_receber()`: % a receber sobre o lucro
- `mes_formatado()`: Retorna "Janeiro/2025" formatado em português
- `dados_grafico()`: Prepara dados para Chart.js

### ✅ Admin (paginas/admin.py)
- **ResultadoFinanceiroMensalAdmin**: Interface administrativa completa
  - Lista com valores coloridos (verde/vermelho/laranja)
  - Filtros por mês e data de criação
  - Campos readonly para metadados
  - Usuário automaticamente salvo ao criar registro
  - Organização em fieldsets temáticos

### ✅ Views (paginas/views.py)

#### 1. `resultados_financeiros(request)`
**URL:** `/financeiro/resultados-mensais/`
**Acesso:** Apenas administradores (@staff_member_required)
**Funcionalidades:**
- Visualização de todos os resultados ou filtro por mês
- Cards resumo com totais gerais
- Gráfico doughnut (Chart.js) com distribuição do mês atual
- Tabela completa com histórico mensal
- Valores coloridos e formatados
- Links para edição no admin Django

#### 2. `exportar_resultados_excel(request)`
**URL:** `/financeiro/resultados-mensais/exportar/`
**Acesso:** Apenas administradores
**Funcionalidades:**
- Exportação para Excel (.xlsx) com openpyxl
- Formatação profissional:
  - Cabeçalhos com fundo laranja (#F56E1D)
  - Valores com cores (verde/vermelho/amarelo)
  - Bordas e alinhamentos
  - Linha de totais com fundo preto
  - Formato monetário R$ #,##0.00
- Filtragem opcional por mês
- Nome do arquivo dinâmico

### ✅ Template (paginas/templates/financeiro/despesas.html)
**Características:**
- ✅ Layout responsivo com Bootstrap 5.3.3
- ✅ Menu lateral integrado com outros módulos
- ✅ Breadcrumb navigation
- ✅ Botão de exportação Excel destacado
- ✅ Filtro de mês com input type="month"
- ✅ 4 cards de resumo com ícones Bootstrap Icons
- ✅ Gráfico doughnut com Chart.js
- ✅ Tabela responsiva com badges coloridos
- ✅ Links diretos para edição no admin
- ✅ Mensagem de acesso restrito para não-staff
- ✅ Estado vazio com call-to-action

---

## 🔧 Instalação e Configuração

### 1. Dependências
Adicione ao `requirements.txt`:
```txt
openpyxl>=3.1.0
```

Instale:
```bash
pip install openpyxl
```

### 2. Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 3. Arquivos Estáticos
```bash
python manage.py collectstatic --noinput
```

---

## 📍 URLs Configuradas

```python
# paginas/urls.py
path('financeiro/resultados-mensais/', views.resultados_financeiros, name='resultados_financeiros'),
path('financeiro/resultados-mensais/exportar/', views.exportar_resultados_excel, name='exportar_resultados_excel'),
```

**Acesso:**
- Visualização: `http://127.0.0.1:8000/financeiro/resultados-mensais/`
- Exportação: `http://127.0.0.1:8000/financeiro/resultados-mensais/exportar/`
- Admin: `http://127.0.0.1:8000/admin/paginas/resultadofinanceiromensal/`

---

## 👨‍💼 Como Usar (Admin)

### 1. Adicionar Resultado Mensal
1. Acesse `/admin/paginas/resultadofinanceiromensal/add/`
2. Selecione o mês (ex: 01/01/2025 para Janeiro/2025)
3. Insira:
   - Lucro Total (ex: 50000.00)
   - Gasto Total (ex: 30000.00)
   - A Receber Total (ex: 15000.00)
4. Adicione observações se necessário
5. Salve

**Resultado:**
- Lucro Líquido = R$ 20.000,00 (calculado automaticamente)
- Usuário criador registrado
- Disponível na página de resultados

### 2. Visualizar Resultados
1. Acesse `/financeiro/resultados-mensais/`
2. Veja:
   - Cards resumo com totais
   - Gráfico doughnut interativo
   - Tabela completa do histórico
3. Filtre por mês específico se necessário
4. Exporte para Excel

### 3. Exportar para Excel
1. Clique no botão "Exportar Excel"
2. Arquivo será baixado automaticamente
3. Abra no Excel/LibreOffice
4. Veja formatação profissional com cores e totais

---

## 🎨 Personalização

### Cores do Gráfico
Em `models.py`, método `dados_grafico()`:
```python
'cores': ['#22c55e', '#ef4444', '#f97316']
# Verde, Vermelho, Laranja
```

### Formato Excel
Em `views.py`, função `exportar_resultados_excel()`:
- `header_fill`: Cor do cabeçalho
- `lucro_fill`: Verde claro para lucros
- `gasto_fill`: Vermelho claro para gastos
- `receber_fill`: Amarelo para a receber

---

## 📊 Exemplo de Dados

### Entrada no Admin:
- **Mês:** Janeiro/2025
- **Lucro Total:** R$ 80.000,00
- **Gasto Total:** R$ 50.000,00
- **A Receber:** R$ 20.000,00
- **Observações:** "Mês com alta demanda de eventos"

### Saída Calculada:
- **Lucro Líquido:** R$ 30.000,00
- **% Gastos:** 62,5%
- **% A Receber:** 25%

### Gráfico Doughnut:
- Lucro Líquido: R$ 30.000,00 (verde)
- Gastos: R$ 50.000,00 (vermelho)
- A Receber: R$ 20.000,00 (laranja)

---

## 🔒 Segurança

### Restrição de Acesso
- ✅ `@staff_member_required`: Apenas usuários com `is_staff=True`
- ✅ Template verifica `{% if user.is_staff %}`
- ✅ Admin Django com autenticação padrão

### Validações
- ✅ `unique=True` no campo `mes` (evita duplicatas)
- ✅ `MinValueValidator(0)` nos valores monetários
- ✅ Usuário criador registrado automaticamente

---

## 📱 Responsividade

### Mobile (≤768px)
- Cards empilhados verticalmente
- Tabela com scroll horizontal
- Gráfico ajustado

### Tablet (769-1024px)
- Cards em grid 2x2
- Tabela responsiva

### Desktop (>1024px)
- Cards em linha (4 colunas)
- Gráfico centralizado
- Tabela completa

---

## 🚀 Próximos Passos (Opcional)

### Melhorias Futuras:
1. **Dashboard com múltiplos gráficos**
   - Gráfico de linha (evolução mensal)
   - Gráfico de barras (comparação ano a ano)

2. **Relatórios automáticos**
   - Email mensal com resumo
   - PDF gerado automaticamente

3. **Previsões**
   - Cálculo de média móvel
   - Projeções para próximos meses

4. **Integração com Mensalidades**
   - Calcular lucro automaticamente com base em pagamentos
   - Sincronizar gastos com despesas cadastradas

5. **Alertas**
   - Notificação se lucro líquido negativo
   - Alerta se gastos > 70% do lucro

---

## 📞 Suporte

Para dúvidas ou problemas:
1. Verifique os logs do Django
2. Confira se migrations foram aplicadas
3. Teste com usuário `is_staff=True`
4. Verifique se openpyxl está instalado

---

## ✅ Checklist de Implementação

- [x] Model `ResultadoFinanceiroMensal` criado
- [x] Admin configurado e funcional
- [x] View `resultados_financeiros` implementada
- [x] View `exportar_resultados_excel` com openpyxl
- [x] Template HTML responsivo e integrado
- [x] URLs configuradas
- [x] Migrations aplicadas
- [x] Gráfico Chart.js implementado
- [x] Exportação Excel com formatação
- [x] Segurança com @staff_member_required
- [x] Documentação completa

---

## 🎉 Sistema Pronto para Uso!

O sistema está **100% funcional** e pronto para gerenciar os resultados financeiros da Giro DNC!

**Acesse:** `http://127.0.0.1:8000/financeiro/resultados-mensais/`
