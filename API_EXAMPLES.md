# Exemplos de Uso da API - Portal do Aluno

## 🔐 Autenticação

A API utiliza Session Authentication. Para consumir a API, o usuário precisa estar autenticado.

### Exemplo com JavaScript (Fetch API):

```javascript
// Login primeiro (através do formulário de login normal)
// Depois pode consumir a API

// Obter CSRF Token
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

const csrftoken = getCookie('csrftoken');
```

## 📊 Exemplos de Requisições

### 1. Dashboard do Aluno

```javascript
// GET /api/painel-aluno/alunos/dashboard/
fetch('/api/painel-aluno/alunos/dashboard/', {
    method: 'GET',
    headers: {
        'Content-Type': 'application/json',
    },
    credentials: 'include'
})
.then(response => response.json())
.then(data => {
    console.log('Dashboard:', data);
    // {
    //   aluno: {...},
    //   turmas: [...],
    //   avisos_recentes: [...],
    //   proximas_aulas: [...],
    //   total_aulas: 50,
    //   presencas: 45,
    //   percentual_presenca: 90.0,
    //   mensalidades_pendentes: [...],
    //   mensagens_nao_lidas: 3
    // }
})
.catch(error => console.error('Erro:', error));
```

### 2. Dados do Aluno Logado

```javascript
// GET /api/painel-aluno/alunos/me/
fetch('/api/painel-aluno/alunos/me/', {
    method: 'GET',
    credentials: 'include'
})
.then(response => response.json())
.then(data => {
    console.log('Aluno:', data);
    // {
    //   id: 1,
    //   usuario: {...},
    //   nome_completo: "João Silva",
    //   cpf: "123.456.789-00",
    //   turmas: [...]
    // }
});
```

### 3. Próximas Aulas

```javascript
// GET /api/painel-aluno/aulas/proximas/
fetch('/api/painel-aluno/aulas/proximas/', {
    method: 'GET',
    credentials: 'include'
})
.then(response => response.json())
.then(data => {
    console.log('Próximas aulas:', data);
    data.forEach(aula => {
        console.log(`${aula.turma_nome} - ${aula.data} ${aula.hora_inicio}`);
    });
});
```

### 4. Horários de Aulas

```javascript
// GET /api/painel-aluno/horarios/
fetch('/api/painel-aluno/horarios/', {
    method: 'GET',
    credentials: 'include'
})
.then(response => response.json())
.then(data => {
    console.log('Horários:', data);
    // Agrupar por dia da semana
    const horariosPorDia = {};
    data.results.forEach(horario => {
        const dia = horario.dia_semana_display;
        if (!horariosPorDia[dia]) {
            horariosPorDia[dia] = [];
        }
        horariosPorDia[dia].push(horario);
    });
});
```

### 5. Estatísticas de Frequência

```javascript
// GET /api/painel-aluno/frequencias/estatisticas/
fetch('/api/painel-aluno/frequencias/estatisticas/', {
    method: 'GET',
    credentials: 'include'
})
.then(response => response.json())
.then(data => {
    console.log('Estatísticas de Frequência:', data);
    data.forEach(stat => {
        console.log(`${stat.turma.nome}: ${stat.percentual_presenca}% de presença`);
    });
});
```

### 6. Avisos

```javascript
// GET /api/painel-aluno/avisos/
fetch('/api/painel-aluno/avisos/', {
    method: 'GET',
    credentials: 'include'
})
.then(response => response.json())
.then(data => {
    console.log('Avisos:', data);
    data.results.forEach(aviso => {
        console.log(`${aviso.titulo} - ${aviso.tipo_display}`);
        if (aviso.importante) {
            console.log('⚠️ AVISO IMPORTANTE!');
        }
    });
});
```

### 7. Mensalidades Pendentes

```javascript
// GET /api/painel-aluno/mensalidades/pendentes/
fetch('/api/painel-aluno/mensalidades/pendentes/', {
    method: 'GET',
    credentials: 'include'
})
.then(response => response.json())
.then(data => {
    console.log('Mensalidades Pendentes:', data);
    let totalPendente = 0;
    data.forEach(mens => {
        totalPendente += parseFloat(mens.valor_final);
        console.log(`${mens.mes_referencia}: R$ ${mens.valor_final} - Vencimento: ${mens.data_vencimento}`);
    });
    console.log(`Total pendente: R$ ${totalPendente.toFixed(2)}`);
});
```

### 8. Mensagens

#### Listar Mensagens Recebidas
```javascript
// GET /api/painel-aluno/mensagens/recebidas/
fetch('/api/painel-aluno/mensagens/recebidas/', {
    method: 'GET',
    credentials: 'include'
})
.then(response => response.json())
.then(data => {
    console.log('Mensagens Recebidas:', data);
});
```

#### Enviar Mensagem
```javascript
// POST /api/painel-aluno/mensagens/
fetch('/api/painel-aluno/mensagens/', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrftoken
    },
    credentials: 'include',
    body: JSON.stringify({
        destinatario: 2,  // ID do destinatário
        assunto: 'Dúvida sobre horário',
        conteudo: 'Gostaria de saber se há possibilidade de trocar o horário da aula.'
    })
})
.then(response => response.json())
.then(data => {
    console.log('Mensagem enviada:', data);
});
```

#### Marcar Mensagem como Lida
```javascript
// POST /api/painel-aluno/mensagens/{id}/marcar_lida/
const mensagemId = 5;
fetch(`/api/painel-aluno/mensagens/${mensagemId}/marcar_lida/`, {
    method: 'POST',
    headers: {
        'X-CSRFToken': csrftoken
    },
    credentials: 'include'
})
.then(response => response.json())
.then(data => {
    console.log('Mensagem marcada como lida:', data);
});
```

#### Contar Mensagens Não Lidas
```javascript
// GET /api/painel-aluno/mensagens/nao_lidas/
fetch('/api/painel-aluno/mensagens/nao_lidas/', {
    method: 'GET',
    credentials: 'include'
})
.then(response => response.json())
.then(data => {
    console.log(`Você tem ${data.nao_lidas} mensagens não lidas`);
    // Atualizar badge de notificação
    document.getElementById('badge-mensagens').textContent = data.nao_lidas;
});
```

## 🐍 Exemplos com Python (requests)

```python
import requests

# URL base
BASE_URL = 'http://localhost:8000'

# Fazer login primeiro
session = requests.Session()
login_data = {
    'username': 'aluno@exemplo.com',
    'password': 'senha123'
}
session.post(f'{BASE_URL}/login/', data=login_data)

# Obter CSRF Token
csrf_token = session.cookies.get('csrftoken')

# Dashboard
response = session.get(f'{BASE_URL}/api/painel-aluno/alunos/dashboard/')
dashboard = response.json()
print(f"Percentual de presença: {dashboard['percentual_presenca']}%")

# Próximas aulas
response = session.get(f'{BASE_URL}/api/painel-aluno/aulas/proximas/')
proximas_aulas = response.json()
for aula in proximas_aulas:
    print(f"Aula: {aula['turma_nome']} - {aula['data']} {aula['hora_inicio']}")

# Enviar mensagem
headers = {'X-CSRFToken': csrf_token}
mensagem_data = {
    'destinatario': 2,
    'assunto': 'Teste',
    'conteudo': 'Mensagem de teste'
}
response = session.post(
    f'{BASE_URL}/api/painel-aluno/mensagens/',
    json=mensagem_data,
    headers=headers
)
print(f"Mensagem enviada: {response.json()}")
```

## 📱 Exemplo com jQuery/AJAX

```javascript
// Dashboard
$.ajax({
    url: '/api/painel-aluno/alunos/dashboard/',
    method: 'GET',
    success: function(data) {
        // Atualizar dashboard
        $('#percentual-presenca').text(data.percentual_presenca + '%');
        $('#total-aulas').text(data.total_aulas);
        $('#mensagens-nao-lidas').text(data.mensagens_nao_lidas);
        
        // Listar próximas aulas
        data.proximas_aulas.forEach(function(aula) {
            $('#lista-aulas').append(
                `<li>${aula.turma_nome} - ${aula.data} ${aula.hora_inicio}</li>`
            );
        });
    },
    error: function(xhr) {
        console.error('Erro:', xhr.responseText);
    }
});

// Enviar mensagem
$('#form-mensagem').submit(function(e) {
    e.preventDefault();
    
    $.ajax({
        url: '/api/painel-aluno/mensagens/',
        method: 'POST',
        headers: {
            'X-CSRFToken': csrftoken
        },
        contentType: 'application/json',
        data: JSON.stringify({
            destinatario: $('#destinatario').val(),
            assunto: $('#assunto').val(),
            conteudo: $('#conteudo').val()
        }),
        success: function(data) {
            alert('Mensagem enviada com sucesso!');
            $('#form-mensagem')[0].reset();
        },
        error: function(xhr) {
            alert('Erro ao enviar mensagem: ' + xhr.responseText);
        }
    });
});
```

## 🔄 Paginação

A API retorna dados paginados. Exemplo de resposta:

```json
{
    "count": 100,
    "next": "http://localhost:8000/api/painel-aluno/aulas/?page=2",
    "previous": null,
    "results": [...]
}
```

Para navegar entre páginas:

```javascript
let currentPage = 1;

function carregarAulas(page = 1) {
    fetch(`/api/painel-aluno/aulas/?page=${page}`, {
        credentials: 'include'
    })
    .then(response => response.json())
    .then(data => {
        // Renderizar aulas
        renderizarAulas(data.results);
        
        // Atualizar botões de paginação
        document.getElementById('btn-anterior').disabled = !data.previous;
        document.getElementById('btn-proximo').disabled = !data.next;
        
        currentPage = page;
    });
}

// Botão próxima página
document.getElementById('btn-proximo').addEventListener('click', () => {
    carregarAulas(currentPage + 1);
});

// Botão página anterior
document.getElementById('btn-anterior').addEventListener('click', () => {
    carregarAulas(currentPage - 1);
});
```

## 🎨 Integração com Templates

Exemplo de como usar a API nos templates HTML existentes:

```html
<script>
document.addEventListener('DOMContentLoaded', function() {
    // Carregar dashboard
    fetch('/api/painel-aluno/alunos/dashboard/')
        .then(response => response.json())
        .then(data => {
            // Atualizar elementos da página
            document.getElementById('nome-aluno').textContent = data.aluno.nome_completo;
            document.getElementById('percentual-presenca').textContent = data.percentual_presenca + '%';
            
            // Carregar avisos
            const listaAvisos = document.getElementById('lista-avisos');
            data.avisos_recentes.forEach(aviso => {
                const item = document.createElement('div');
                item.className = aviso.importante ? 'aviso importante' : 'aviso';
                item.innerHTML = `
                    <h4>${aviso.titulo}</h4>
                    <p>${aviso.conteudo}</p>
                    <small>${aviso.data_criacao}</small>
                `;
                listaAvisos.appendChild(item);
            });
        });
    
    // Atualizar mensagens não lidas a cada 30 segundos
    setInterval(() => {
        fetch('/api/painel-aluno/mensagens/nao_lidas/')
            .then(response => response.json())
            .then(data => {
                document.getElementById('badge-mensagens').textContent = data.nao_lidas;
            });
    }, 30000);
});
</script>
```

## 🚨 Tratamento de Erros

```javascript
fetch('/api/painel-aluno/alunos/dashboard/')
    .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
    })
    .then(data => {
        // Processar dados
    })
    .catch(error => {
        console.error('Erro ao carregar dashboard:', error);
        // Mostrar mensagem de erro para o usuário
        alert('Erro ao carregar dados. Por favor, tente novamente.');
    });
```

---

**Desenvolvido para GIRO DNC** 🎭💃
