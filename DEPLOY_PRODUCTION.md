# 📦 Deploy em Produção - Giro DNC

## ✅ O que foi feito (Estrutura Correta)

Reorganizamos os arquivos estáticos para seguir a **estrutura padrão do Django**:

### Antes (❌ Errado):
```
staticfiles/           # Pasta de produção usada como fonte
  ├── style.css
  ├── js/
  └── IMG/

STATICFILES_DIRS = [BASE_DIR / "staticfiles"]  # ❌ Apontando para destino
STATIC_ROOT = BASE_DIR / 'staticfiles_collected'
```

### Agora (✅ Correto):
```
paginas/
  └── static/
      └── paginas/      # Namespace da app
          ├── css/
          │   ├── style.css
          │   ├── mensalidades.css
          │   ├── extrato.css
          │   └── despesas.css
          ├── js/
          │   ├── script.js
          │   └── mensalidade.js
          └── img/
              ├── Girologo.jpg
              ├── Mensalidades.png
              └── ...

# settings.py
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / 'staticfiles'  # Destino do collectstatic
# STATICFILES_DIRS removido - Django busca automaticamente em app/static/
```

---

## 🚀 Como fazer deploy em PRODUÇÃO

### 1️⃣ Configure as variáveis de ambiente

Crie um arquivo `.env` ou configure no servidor:

```bash
SECRET_KEY=sua-chave-secreta-aleatoria-muito-longa
DEBUG=False
ALLOWED_HOSTS=seu-dominio.com,www.seu-dominio.com
DATABASE_URL=postgresql://user:pass@localhost/dbname  # Se usar PostgreSQL
```

### 2️⃣ Atualize o settings.py para produção

```python
import os
from pathlib import Path

SECRET_KEY = os.environ.get('SECRET_KEY', 'fallback-key-nunca-use-em-prod')
DEBUG = os.environ.get('DEBUG', 'False') == 'True'
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '').split(',')

# Configurações de segurança
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

# Arquivos estáticos
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
```

### 3️⃣ Execute o collectstatic

**Este é o comando FUNDAMENTAL para produção:**

```bash
python manage.py collectstatic --noinput
```

**O que esse comando faz:**
- ✅ Busca arquivos em `paginas/static/paginas/`
- ✅ Busca arquivos em `login/static/login/`
- ✅ Busca arquivos do Django Admin em `django/contrib/admin/static/`
- ✅ **Copia TUDO** para `staticfiles/` (pasta de produção)
- ✅ Organiza: `staticfiles/paginas/css/style.css`, `staticfiles/admin/css/base.css`, etc.

**Resultado:**
```
64 static files copied to '/workspaces/giro-dnc/staticfiles', 132 unmodified.
```

### 4️⃣ Configure o servidor web (Nginx/Apache)

**Exemplo com Nginx:**

```nginx
server {
    listen 80;
    server_name seu-dominio.com;

    # Servir arquivos estáticos diretamente
    location /static/ {
        alias /caminho/para/seu-projeto/staticfiles/;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }

    # Servir arquivos de mídia (uploads)
    location /media/ {
        alias /caminho/para/seu-projeto/media/;
    }

    # Proxy para Django (Gunicorn/uWSGI)
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### 5️⃣ Use Gunicorn ou uWSGI

**Instale o Gunicorn:**
```bash
pip install gunicorn
```

**Rode o Django com Gunicorn:**
```bash
gunicorn giro_dance.wsgi:application --bind 0.0.0.0:8000 --workers 4
```

**Ou crie um serviço systemd** (`/etc/systemd/system/giro-dnc.service`):
```ini
[Unit]
Description=Giro DNC Django App
After=network.target

[Service]
User=seu-usuario
Group=www-data
WorkingDirectory=/caminho/para/seu-projeto
Environment="PATH=/caminho/para/venv/bin"
Environment="SECRET_KEY=sua-chave-secreta"
Environment="DEBUG=False"
ExecStart=/caminho/para/venv/bin/gunicorn \
          --workers 4 \
          --bind 127.0.0.1:8000 \
          giro_dance.wsgi:application

[Install]
WantedBy=multi-user.target
```

**Ative o serviço:**
```bash
sudo systemctl daemon-reload
sudo systemctl start giro-dnc
sudo systemctl enable giro-dnc
```

---

## 🔄 Quando você fizer mudanças nos arquivos estáticos

### Em DESENVOLVIMENTO (local):
- ✅ Edite os arquivos em `paginas/static/paginas/css/style.css`
- ✅ O Django serve automaticamente de `paginas/static/`
- ✅ Não precisa rodar `collectstatic` (apenas em dev)

### Em PRODUÇÃO (servidor):
1. Faça as mudanças nos arquivos em `paginas/static/paginas/`
2. Commit e push para o repositório
3. No servidor, faça pull das mudanças
4. **SEMPRE execute:**
   ```bash
   python manage.py collectstatic --noinput
   ```
5. Reinicie o Gunicorn:
   ```bash
   sudo systemctl restart giro-dnc
   ```

---

## 📋 Checklist de Deploy

- [ ] Configurar variáveis de ambiente (SECRET_KEY, DEBUG=False)
- [ ] Atualizar ALLOWED_HOSTS com domínio de produção
- [ ] Configurar banco de dados de produção (PostgreSQL/MySQL)
- [ ] Rodar migrações: `python manage.py migrate`
- [ ] **Rodar collectstatic: `python manage.py collectstatic --noinput`**
- [ ] Criar superusuário: `python manage.py createsuperuser`
- [ ] Configurar Nginx/Apache para servir `/static/` e `/media/`
- [ ] Instalar e configurar Gunicorn/uWSGI
- [ ] Configurar SSL (Let's Encrypt/Certbot)
- [ ] Configurar backups automáticos do banco
- [ ] Configurar logs de erro
- [ ] Testar todas as páginas em produção

---

## 🎯 Resumo: O que você precisa fazer

### **Durante o desenvolvimento (local):**
✅ Nada! Apenas edite os arquivos em `paginas/static/paginas/`

### **Ao fazer deploy (produção):**
```bash
# 1. Faça pull das mudanças
git pull origin main

# 2. Ative o ambiente virtual
source venv/bin/activate

# 3. Instale dependências
pip install -r requirements.txt

# 4. Rode migrações
python manage.py migrate

# 5. 🔥 SEMPRE rode collectstatic 🔥
python manage.py collectstatic --noinput

# 6. Reinicie o servidor
sudo systemctl restart giro-dnc
```

---

## ❓ FAQ

**P: Preciso rodar collectstatic toda vez que fizer deploy?**  
R: SIM! Sempre que você mudar CSS, JS ou imagens.

**P: E se eu esquecer de rodar collectstatic?**  
R: Seus arquivos novos não vão aparecer. O Nginx serve de `staticfiles/`, e se você não rodar collectstatic, os arquivos antigos ficam lá.

**P: Posso deletar a pasta `staticfiles/` no servidor?**  
R: Não! É ela que o Nginx/Apache usa para servir os arquivos. Você pode deletar e rodar `collectstatic` de novo se precisar.

**P: Por que 64 arquivos copiados e 132 não modificados?**  
R: Django Admin tem MUITOS arquivos estáticos (CSS, JS, imagens). Eles já estavam copiados. Apenas os seus 64 arquivos foram copiados agora.

---

## 🎉 Estrutura Final

```
giro-dnc/
├── paginas/
│   ├── static/
│   │   └── paginas/          # ✅ Arquivos FONTE (você edita aqui)
│   │       ├── css/
│   │       ├── js/
│   │       └── img/
│   └── templates/
│       └── painel/
│           └── index.html    # {% static 'paginas/css/style.css' %}
│
├── staticfiles/              # ✅ Arquivos DESTINO (collectstatic gera)
│   ├── paginas/              # Copiado de paginas/static/paginas/
│   │   ├── css/
│   │   ├── js/
│   │   └── img/
│   └── admin/                # Copiado do Django Admin
│       ├── css/
│       └── js/
│
└── giro_dance/
    └── settings.py
        STATIC_URL = "/static/"
        STATIC_ROOT = BASE_DIR / 'staticfiles'  # ✅ Correto!
```

**Funcionamento:**
1. **Desenvolvimento:** Django serve de `paginas/static/paginas/` automaticamente
2. **Produção:** Nginx serve de `staticfiles/` (gerado por `collectstatic`)

---

**Agora está tudo conforme a documentação oficial do Django! 🎉**

Documentação oficial: https://docs.djangoproject.com/en/5.2/howto/static-files/
