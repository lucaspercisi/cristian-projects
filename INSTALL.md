# 🚀 Guia de Instalação e Deploy

## Instalação Local

### 1. Instalar Dependências

```bash
pip install -r requirements.txt
```

### 2. Configurar PostgreSQL

#### Windows:
1. Baixe e instale PostgreSQL: https://www.postgresql.org/download/windows/
2. Crie o banco de dados:
```sql
createdb sistema_login
```

#### Linux/Mac:
```bash
sudo apt-get install postgresql
createdb sistema_login
```

### 3. Configurar Variáveis de Ambiente

Copie o arquivo `.env.example` para `.env` e edite com suas configurações:

```bash
cp .env.example .env
```

### 4. Inicializar Banco de Dados

```bash
python init_database.py
```

Isso irá criar:
- Todas as tabelas necessárias
- Usuário admin (admin / admin123)
- Sistema de permissões

### 5. Executar a Aplicação

```bash
python app_new.py
```

Acesse: http://localhost:5000

---

## 🚀 Deploy em Produção

### Opção 1: Render.com (Recomendado - Gratuito)

1. Faça push do código para GitHub
2. Acesse https://render.com
3. Conecte seu repositório GitHub
4. Configure:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python app_new.py`
   - **Environment**: Python 3
5. Adicione variáveis de ambiente:
   ```
   FLASK_ENV=production
   SECRET_KEY=sua-chave-secreta-aqui
   DATABASE_URL=postgresql://user:pass@host:5432/dbname
   ```

### Opção 2: Railway.app

1. Acesse https://railway.app
2. Importe projeto do GitHub
3. Adicione PostgreSQL como serviço
4. Configure as variáveis de ambiente
5. Deploy automático!

### Opção 3: Heroku

1. Instale Heroku CLI
2. Login: `heroku login`
3. Criar app: `heroku create`
4. Adicionar PostgreSQL: `heroku addons:create heroku-postgresql:hobby-dev`
5. Deploy: `git push heroku main`

### Opção 4: AWS/Azure (Corporativo)

Siga a documentação específica de cada plataforma.

---

## 📊 Melhorias Implementadas

### ✅ Arquitetura Escalável
- **SQLAlchemy ORM**: Substituição de SQL puro
- **Flask-Login**: Autenticação profissional
- **Flask-Principal**: Sistema de permissões
- **Alembic**: Migrações de banco de dados

### ✅ Segurança
- Senhas hasheadas com bcrypt
- Variáveis de ambiente
- Proteção CSRF
- Sessões seguras

### ✅ Deploy na Nuvem
- Configuração para produção
- Suporte a múltiplos provedores
- Health checks
- Logs estruturados

---

## 🔧 Configuração Pós-Deploy

1. Acesse o sistema com: admin / admin123
2. Mude a senha do admin imediatamente
3. Configure permissões para outros usuários
4. Importe dados iniciais se necessário

---

## 📝 Notas Importantes

- Em produção, **NUNCA** use senhas padrão
- Configure backup automático do banco
- Use HTTPS em produção
- Monitore logs e performance
- Configure alertas de erro

