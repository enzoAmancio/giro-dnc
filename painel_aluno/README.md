# Painel do Aluno - GIRO DNC

Esta pasta contém todo o sistema do painel do aluno da escola de dança GIRO DNC.

## Estrutura de Arquivos

```
painel_aluno/
├── css/
│   └── style.css           # Estilos principais do painel
├── js/
│   └── script.js           # JavaScript para interatividade
├── index.html              # Visão geral do painel (dashboard)
├── horarios_aula.html      # Página de horários de aula
├── avisos.html             # Página de avisos
├── minhas_aulas.html       # Página das aulas matriculadas
├── comunicacao.html        # Página de contato
├── chat.html               # Página de chat
└── README.md               # Este arquivo
```

## Páginas Disponíveis

### 1. **Visão Geral** (`index.html`)
Dashboard principal com:
- Cards de próximas aulas
- Avisos importantes
- Status financeiro
- Estatísticas de frequência
- Calendário de aulas

### 2. **Horários de Aula** (`horarios_aula.html`)
Exibe os horários das aulas:
- Jazz Class (Sexta-feira 18:00-19:00)
- Jazz Funk (Sábado 18:00-19:00)
- Treino Competitivo (Domingo 8:00-9:00)

### 3. **Avisos** (`avisos.html`)
Central de avisos e comunicados da escola.

### 4. **Minhas Aulas** (`minhas_aulas.html`)
Lista das aulas em que o aluno está matriculado.

### 5. **Comunicação** (`comunicacao.html`)
Página para entrar em contato com a escola.

### 6. **Chat** (`chat.html`)
Sistema de chat (em desenvolvimento).

## Funcionalidades

### Menu Lateral
- **Desktop**: Colapse/expansão com ícones
- **Mobile**: Menu overlay que desliza da lateral
- Links organizados em categorias:
  - Painel do aluno
  - Financeiro (links para outras seções)
  - Minhas aulas
  - Comunicação

### Responsividade
- Layout totalmente responsivo
- Menu adaptativo para mobile/desktop
- Cards que se reorganizam conforme o tamanho da tela

### Calendário Interativo
- Navegação entre meses
- Destaque dos dias com aulas
- Gerado dinamicamente via JavaScript

## Links Externos

O menu lateral inclui links para outras seções do sistema:
- **Financeiro**: Mensalidades, Extrato, Despesas (`../Financeiro/HTML/`)
- **Home**: Página inicial (`../GIROHOME/index.html`)

## Tecnologias Utilizadas

- **HTML5**: Estrutura semântica
- **CSS3**: Estilos e responsividade
- **Bootstrap 5**: Framework CSS e componentes
- **Bootstrap Icons**: Iconografia
- **JavaScript**: Interatividade e funcionalidades dinâmicas
- **Google Fonts**: Tipografia (Montserrat)

## Como Usar

1. Abra qualquer arquivo HTML no navegador
2. O menu lateral permite navegar entre as seções
3. No mobile, use o botão de menu (☰) para abrir/fechar o menu
4. Todos os links estão funcionais e interconectados

## Personalização

### Cores
As cores principais estão definidas em variáveis CSS em `css/style.css`:
- Laranja principal: `#f97316`
- Fundo escuro: `#000`
- Cinza claro: `#f1f5f9`

### Adicionando Novas Páginas
1. Crie o arquivo HTML seguindo a estrutura das páginas existentes
2. Copie o menu lateral de qualquer página
3. Atualize o link ativo no menu
4. Adicione o link nas outras páginas se necessário