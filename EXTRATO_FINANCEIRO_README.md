# 📊 Sistema de Extrato Financeiro

## ✅ O que foi implementado:

### 1. **Página de Extrato Dinâmica**
📄 **Arquivo:** `paginas/templates/financeiro/Extrato.html`

**Funcionalidades:**
- ✅ Tabela com todas as mensalidades (últimas 12)
- ✅ Exibe: Mês/Ano, Vencimento, Valor Original, Desconto, Valor Final, Data Pagamento, Status, Forma Pagamento
- ✅ Badges coloridos para status:
  - 🟢 Verde = PAGO
  - 🟡 Amarelo = PENDENTE
  - 🔴 Vermelho = ATRASADO
- ✅ Botão "Exportar CSV" no topo da página
- ✅ Responsivo (funciona em mobile)

---

### 2. **Exportação em CSV**
📥 **Funcionalidade:** Download do extrato completo

**O que o CSV contém:**
```csv
Mês/Ano;Data Vencimento;Valor Original;Desconto;Valor Final;Data Pagamento;Status;Forma Pagamento;Observações
10/2024;15/10/2024;R$ 150,00;R$ 0,00;R$ 150,00;20/10/2024;Pago;Pix;-
11/2024;15/11/2024;R$ 150,00;R$ 15,00;R$ 135,00;-;Pendente;-;-

TOTAIS
Total Pago;;;;R$ 150,00
Total Pendente;;;;R$ 135,00
```

**Características do CSV:**
- ✅ Formato compatível com Excel (UTF-8 com BOM)
- ✅ Delimitador: `;` (ponto e vírgula)
- ✅ Valores monetários formatados (R$ X,XX)
- ✅ Datas formatadas (dd/mm/aaaa)
- ✅ Linha de totais no final
- ✅ Nome do arquivo: `extrato_financeiro_<username>.csv`

---

### 3. **Views Criadas**

#### `financeiro_extrato(request)` - Linha 345
**O que faz:**
- Busca mensalidades do aluno logado
- Ordena por mês (mais recente primeiro)
- Limita a 12 mensalidades
- Envia para o template

#### `financeiro_extrato_csv(request)` - Linha 362
**O que faz:**
- Gera arquivo CSV
- Formata dados para Excel
- Calcula totais automaticamente
- Faz download direto

---

### 4. **Rota Adicionada**
📍 **Arquivo:** `paginas/urls.py`

```python
path('financeiro/extrato/csv/', views.financeiro_extrato_csv, name='financeiro_extrato_csv'),
```

**URL completa:** `http://127.0.0.1:8000/financeiro/extrato/csv/`

---

## 🚀 Como usar:

### **Para o Aluno:**

1. **Acessar o extrato:**
   ```
   http://127.0.0.1:8000/financeiro/extrato/
   ```

2. **Ver todas as mensalidades na tabela**
   - Cores indicam status
   - Valores formatados em Real

3. **Exportar CSV:**
   - Clique no botão "Exportar CSV"
   - Arquivo baixa automaticamente
   - Abrir no Excel ou Google Sheets

---

### **Para o Admin (Portal de Transparência):**

#### **Próximo passo:** Criar página de despesas

**O que precisa ter:**
1. Tabela com todas as despesas da escola
2. Categorias: Aluguel, Luz, Água, Professores, Material, etc.
3. Filtros por mês/ano
4. Gráficos de gastos
5. Exportação CSV também

**Modelo sugerido para Despesas:**
```python
class Despesa(models.Model):
    CATEGORIAS = [
        ('ALUGUEL', 'Aluguel'),
        ('ENERGIA', 'Energia Elétrica'),
        ('AGUA', 'Água'),
        ('INTERNET', 'Internet'),
        ('FOLHA', 'Folha de Pagamento'),
        ('MATERIAL', 'Material'),
        ('MANUTENCAO', 'Manutenção'),
        ('MARKETING', 'Marketing'),
        ('OUTROS', 'Outros'),
    ]
    
    categoria = models.CharField(max_length=20, choices=CATEGORIAS)
    descricao = models.CharField(max_length=200)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    data_vencimento = models.DateField()
    data_pagamento = models.DateField(null=True, blank=True)
    mes_referencia = models.DateField()
    pago = models.BooleanField(default=False)
    observacoes = models.TextField(blank=True)
    comprovante = models.FileField(upload_to='despesas/', blank=True, null=True)
```

---

## 📋 Campos da Mensalidade (já existentes):

```python
class Mensalidade:
    aluno = ForeignKey(Aluno)
    mes_referencia = DateField()          # Mês/ano da mensalidade
    valor = DecimalField()                # Valor original
    valor_desconto = DecimalField()       # Desconto aplicado
    valor_final = DecimalField()          # Valor após desconto
    data_vencimento = DateField()         # Quando vence
    data_pagamento = DateField()          # Quando foi pago
    status = CharField()                  # PENDENTE/PAGO/ATRASADO/CANCELADO
    forma_pagamento = CharField()         # Pix, Cartão, etc.
    observacoes = TextField()             # Notas adicionais
```

---

## 🎨 Cores e Badges:

- **🟢 Verde (PAGO):** `badge bg-success`
- **🟡 Amarelo (PENDENTE):** `badge bg-warning`
- **🔴 Vermelho (ATRASADO):** `badge bg-danger`
- **⚫ Cinza (CANCELADO):** `badge bg-secondary`

---

## 📱 Responsividade:

A tabela é responsiva! Em mobile:
- Colunas viram linhas
- Cada célula mostra seu label
- Scroll horizontal quando necessário

---

## ✅ Checklist de Testes:

- [ ] Acessar `/financeiro/extrato/`
- [ ] Ver mensalidades na tabela
- [ ] Verificar badges de status
- [ ] Clicar em "Exportar CSV"
- [ ] Abrir CSV no Excel
- [ ] Verificar formatação brasileira (R$, vírgulas)
- [ ] Ver totais no final do CSV

---

## 🔜 Próximos passos sugeridos:

1. **Criar model Despesa** (modelo acima)
2. **Página de despesas públicas** (transparência)
3. **Dashboard administrativo** com gráficos
4. **Filtros** por data no extrato
5. **Gráfico de evolução** dos pagamentos
6. **Notificações** de vencimento próximo
7. **Comprovantes** de pagamento (upload PDF)

---

## 🐛 Troubleshooting:

**CSV abre com caracteres estranhos no Excel?**
- Está usando BOM UTF-8 (✅ já implementado)
- Abrir: Excel → Dados → De Texto/CSV → UTF-8

**Totais não aparecem no CSV?**
- Os totais estão nas últimas linhas do arquivo
- Role até o fim

**Botão exportar não funciona?**
- Verifique se está logado como aluno
- Verifique URL: `/financeiro/extrato/csv/`

---

## 📊 Exemplo Visual:

### Tabela na página:
```
┌─────────┬──────────────┬──────────┬──────────┬────────┬────────┐
│ Mês/Ano │ Vencimento   │ Valor    │ Desconto │ Final  │ Status │
├─────────┼──────────────┼──────────┼──────────┼────────┼────────┤
│ 10/2024 │ 15/10/2024   │ R$ 150   │ R$ 0     │ R$ 150 │ 🟢 PAGO│
│ 11/2024 │ 15/11/2024   │ R$ 150   │ R$ 15    │ R$ 135 │ 🟡 PEND│
│ 12/2024 │ 15/12/2024   │ R$ 150   │ R$ 0     │ R$ 150 │ 🔴 ATRA│
└─────────┴──────────────┴──────────┴──────────┴────────┴────────┘
```

---

**Documentação criada em:** 06/11/2025  
**Versão:** 1.0  
**Autor:** Sistema Giro DNC
