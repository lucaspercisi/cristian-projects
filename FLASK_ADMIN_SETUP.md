# 🎛️ Flask-Admin: Dashboard de Administração

## O que é o Flask-Admin?

O Flask-Admin é uma interface de administração completa para aplicações Flask - equivalente ao Django Admin!

### Recursos Incluídos:
- ✅ **CRUD completo** (Create, Read, Update, Delete)
- ✅ **Busca e filtros** avançados
- ✅ **Export para CSV/JSON**
- ✅ **Paginação** automática
- ✅ **Interface moderna** (Bootstrap 3)
- ✅ **Segurança** integrada
- ✅ **Upload de arquivos**
- ✅ **Edição inline**

---

## 🚀 Como Acessar

### Desenvolvimento (sem banco configurado ainda)
O admin não aparece porque o PostgreSQL não está configurado.

### Produção (com PostgreSQL)
1. Configure o PostgreSQL
2. Execute `python init_database.py`
3. Inicie o app: `python app_new.py`
4. Acesse: **http://localhost:5000/admin**

---

## 📊 Modelos Disponíveis no Admin

### 1. **Pessoas** (`/admin/pessoa/`)
- Cadastro completo de clientes, fornecedores, etc.
- Busca por: nome, razão social, CPF/CNPJ, cidade, email
- Filtros por: tipo, cidade, contribuinte

### 2. **Produtos** (`/admin/produto/`)
- Gestão de produtos
- Busca por: nome, código de barras, descrição
- Filtros por: origem internacional

### 3. **Contas a Receber** (`/admin/contareceber/`)
- Lançamentos a receber
- Busca por: documento, chave NFe
- Filtros por: status, data

### 4. **Contas a Pagar** (`/admin/contapagar/`)
- Lançamentos a pagar
- Busca por: documento
- Filtros por: status, data

### 5. **Usuários** (`/admin/user/`)
- Gestão de usuários do sistema
- Permissões e perfis

---

## 💡 Personalizando o Admin

### Adicionar Novo Modelo
Edite `admin.py`:

```python
from models import NovoModelo

class NovoModeloView(CustomModelView):
    """View customizada para NovoModelo"""
    
    column_list = ['id', 'nome', 'data']
    column_searchable_list = ['nome', 'descricao']
    column_filters = ['data', 'status']

# Adicionar no init_admin
admin.add_view(NovoModeloView(NovoModelo, db.session, name='Novo Modelo'))
```

### Configurar Permissões
```python
class SecureModelView(CustomModelView):
    """View com restrições de permissão"""
    
    # Apenas admins podem criar/editar
    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_admin
    
    # Sem deletar
    can_delete = False
```

### Adicionar Ações Customizadas
```python
from flask_admin import expose
from flask import request

class PessoaModelView(CustomModelView):
    
    @action('enviar_email', 'Enviar Email', 'Enviar email para selecionados?')
    def action_enviar_email(self, ids):
        # Sua lógica aqui
        for id in ids:
            pessoa = Pessoa.query.get(id)
            enviar_email(pessoa.email)
        
        flash(f'{len(ids)} emails enviados!')
```

---

## 🎨 Temas Disponíveis

Flask-Admin suporta múltiplos temas:

### Bootstrap 3 (padrão atual)
```python
Admin(app, template_mode='bootstrap3')
```

### Bootstrap 2
```python
Admin(app, template_mode='bootstrap2')
```

### AdminLTE (Moderno!)
```bash
pip install flask-adminlte
```

```python
from flask_adminlte import AdminLTE
AdminLTE(app, skin='blue')
```

---

## 🔒 Segurança

### Proteger Admin com Autenticação

```python
from flask_login import login_required, current_user

class SecureModelView(CustomModelView):
    def is_accessible(self):
        # Apenas usuários autenticados
        return current_user.is_authenticated
    
    def _handle_view(self, name, **kwargs):
        # Redirecionar para login se não autenticado
        if not self.is_accessible():
            return redirect(url_for('auth.login'))
```

### Restringir por Permissões
```python
def is_accessible(self):
    return (current_user.is_authenticated and 
            current_user.has_permission('admin'))
```

---

## 📈 Recursos Avançados

### 1. Edição em Tabela (Inline)
```python
class PessoaModelView(CustomModelView):
    inline_models = [
        (EnderecoModel, {
            'form_columns': ['rua', 'cidade'],
        }),
    ]
```

### 2. Relacionamentos
```python
class PessoaModelView(CustomModelView):
    column_list = ['nome', 'produtos']  # Mostra relacionamento
```

### 3. Upload de Arquivos
```python
class ProdutoModelView(CustomModelView):
    form_overrides = {
        'foto': FileUploadField
    }
    
    form_extra_fields = {
        'foto': FileUploadField('Foto do Produto')
    }
```

### 4. Calendário/Datepicker
```python
form_widget_args = {
    'data_vencimento': {
        'class': 'date',
        'data-date-format': 'dd/mm/yyyy'
    }
}
```

---

## 🎯 Comparação: Django Admin vs Flask-Admin

| Feature | Django Admin | Flask-Admin | Vencedor |
|---------|--------------|-------------|----------|
| CRUD Completo | ✅ | ✅ | Empate |
| Busca | ✅ | ✅ | Empate |
| Filtros | ✅ | ✅ | Empate |
| Export | ✅ | ✅ | Empate |
| Themes | ✅ | ✅ | Empate |
| Permissões | ✅ | ✅ | Empate |
| Upload Files | ✅ | ✅ | Empate |
| Inline Editing | ✅ | ✅ | Empate |
| **Flexibilidade** | ❌ | ✅ | Flask-Admin |
| **Customização** | Limitada | Total | Flask-Admin |

**Resultado**: Flask-Admin = Django Admin + Maior Flexibilidade!

---

## 🚀 Próximos Passos

### 1. Habilitar Admin (quando PostgreSQL estiver configurado)
```python
# Descomente em app_new.py:
db.init_app(app)
init_admin(app, db)
```

### 2. Adicionar Mais Modelos
Edite `admin.py` para adicionar seus models!

### 3. Customizar Views
Configure colunas, busca, filtros conforme necessidade.

### 4. Proteger com Autenticação
Adicione `@login_required` e validações de permissão.

---

## 📚 Documentação Oficial

- **Flask-Admin**: https://flask-admin.readthedocs.io/
- **Exemplos**: https://github.com/flask-admin/flask-admin/tree/master/examples
- **Plugins**: https://flask-admin.readthedocs.io/en/latest/plugins/

---

## ✅ Conclusão

Você agora tem um **admin panel completo** no Flask, equivalente ao Django Admin, com ainda **mais flexibilidade**!

**Acesse**: `/admin` quando o PostgreSQL estiver configurado!

