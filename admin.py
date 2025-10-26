"""
Flask-Admin configuração
Equivale ao Django Admin - Dashboard completo!
"""
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_admin import expose
from flask import redirect, url_for

class CustomModelView(ModelView):
    """View customizado com configurações padrão"""
    
    # Página de lista
    page_size = 50
    can_export = True
    can_view_details = True
    
    # Criar/Editar
    can_create = True
    can_edit = True
    can_delete = True
    
    # Busca
    column_searchable_list = []
    column_filters = []
    
class PessoaModelView(CustomModelView):
    """View para Cadastro de Pessoas"""
    
    column_list = [
        'codigo_cadastro', 'nome_completo', 'razao_social', 
        'tipo', 'cidade', 'telefone_celular', 'email'
    ]
    column_searchable_list = [
        'nome_completo', 'razao_social', 'cpf_cnpj', 'email', 'cidade'
    ]
    column_filters = ['tipo', 'cidade', 'contribuinte']
    
    form_excluded_columns = ['created_at', 'updated_at']

class ProdutoModelView(CustomModelView):
    """View para Produtos"""
    
    column_list = [
        'id', 'nome', 'codigo_barras', 'preco_custo', 
        'preco_venda', 'quantidade_estoque'
    ]
    column_searchable_list = ['nome', 'codigo_barras', 'descricao']
    column_filters = ['origem_internacional']

class ContaReceberModelView(CustomModelView):
    """View para Contas a Receber"""
    
    column_list = [
        'codigo_lancamento', 'numero_documento', 'valor_total',
        'data_emissao', 'status'
    ]
    column_searchable_list = ['numero_documento', 'chave_nfe']
    column_filters = ['status', 'data_emissao']

class ContaPagarModelView(CustomModelView):
    """View para Contas a Pagar"""
    
    column_list = [
        'codigo_lancamento', 'numero_documento', 'valor_total',
        'data_vencimento', 'status'
    ]
    column_searchable_list = ['numero_documento']
    column_filters = ['status', 'data_vencimento']

def init_admin(app, db):
    """Inicializa Flask-Admin"""
    
    try:
        # Importar models apenas quando necessário
        from models import User, Pessoa, Produto, ContaReceber, ContaPagar
        
        admin = Admin(
            app, 
            name='Sistema de Gestao',
            template_mode='bootstrap3'
        )
        
        # Adicionar views
        admin.add_view(PessoaModelView(Pessoa, db.session, name='Pessoas', category='Cadastros'))
        admin.add_view(ProdutoModelView(Produto, db.session, name='Produtos', category='Cadastros'))
        admin.add_view(ContaReceberModelView(ContaReceber, db.session, name='Contas a Receber', category='Financeiro'))
        admin.add_view(ContaPagarModelView(ContaPagar, db.session, name='Contas a Pagar', category='Financeiro'))
        admin.add_view(CustomModelView(User, db.session, name='Usuários', category='Configurações'))
        
        print("[OK] Flask-Admin inicializado com sucesso!")
        print("[WEB] Acesse: http://localhost:5000/admin")
        
        return admin
        
    except Exception as e:
        print(f"[ERRO] Falha ao inicializar Flask-Admin: {e}")
        print("[INFO] Admin nao estara disponivel (banco nao configurado)")
        return None

