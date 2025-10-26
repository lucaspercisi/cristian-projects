"""
Aplicação Flask principal - Versão Escalável
"""
from flask import Flask
from flask_login import LoginManager, login_required
from config import config
from models import db, User
import os

def create_app(config_name=None):
    """Factory para criar a aplicação Flask"""
    app = Flask(__name__)
    
    # Carregar configuração
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'development')
    
    app.config.from_object(config[config_name])
    
    # Inicializar extensões
    # Temporariamente comentado - precisa do PostgreSQL configurado
    # db.init_app(app)
    
    # Configurar Flask-Login
    # Temporariamente comentado - precisa do banco configurado
    # login_manager = LoginManager()
    # login_manager.init_app(app)
    # login_manager.login_view = 'auth.login'
    # login_manager.login_message = 'Por favor, faça login para acessar esta página.'
    # login_manager.login_message_category = 'info'
    
    # @login_manager.user_loader
    # def load_user(user_id):
    #     """Callback para carregar usuário"""
    #     return User.query.get(int(user_id))
    
    # Registrar blueprints
    from auth import init_auth
    init_auth(app)
    
    # Configurar Flask-Admin (dashboard completo!)
    try:
        from admin import init_admin
        # Só inicializa se o banco estiver configurado
        if hasattr(app, 'config') and app.config.get('SQLALCHEMY_DATABASE_URI'):
            init_admin(app, db)
    except Exception as e:
        print(f"[AVISO] Admin nao inicializado: {e}")
        print("[INFO] Configure o PostgreSQL para usar o admin panel")
    
    # Importar e registrar outras rotas
    register_routes(app)
    
    # Shell context para flask shell
    # Temporariamente comentado
    # @app.shell_context_processor
    # def make_shell_context():
    #     return {'db': db, 'User': User}
    
    return app

def register_routes(app):
    """Registra todas as rotas da aplicação"""
    
    @app.route('/')
    def index():
        from flask import redirect, url_for
        return redirect(url_for('dashboard'))
    
    @app.route('/dashboard')
    def dashboard():
        # Deixar sem @login_required temporariamente para testar
        from flask import render_template
        return render_template('dashboard.html')
    
    # Rotas de cadastro
    @app.route('/cadastrar_geral', methods=['GET', 'POST'])
    # @login_required
    def cadastrar_geral():
        from flask import render_template, request, flash
        # Temporariamente comentado - precisa do PostgreSQL configurado
        # from models import Pessoa
        # from datetime import datetime
        
        sucesso = None
        erro = None
        proximo_codigo = 1
        
        # Funcionalidade de banco comentada temporariamente
        # Voltará quando PostgreSQL estiver configurado
        try:
            if request.method == 'POST':
                # Pega os dados mas não salva ainda
                dados_recebidos = {
                    'codigo_cadastro': request.form.get('codigo_cadastro'),
                    'tipo': request.form.get('tipo'),
                }
                sucesso = "POST recebido! (Banco de dados não configurado ainda)"
            
            # Calcular próximo código simulado
            proximo_codigo = 1
            
        except Exception as e:
            erro = f"Erro: {str(e)}"
        
        return render_template('cadastro_geral.html', sucesso=sucesso, erro=erro, proximo_codigo=proximo_codigo)
    
    # Temporariamente comentamos @login_required para testar sem autenticação
    # from flask_login import login_required
    
    # Registra rotas básicas do sistema original
    @app.route('/cadastrar_produtos', methods=['GET', 'POST'])
    # @login_required
    def cadastrar_produtos():
        from flask import render_template
        return render_template('cadastro_produtos.html')
    
    @app.route('/cadastrar_servicos', methods=['GET', 'POST'])
    # @login_required
    def cadastrar_servicos():
        from flask import render_template
        return render_template('cadastro_servicos.html')
    
    @app.route('/contas_a_receber', methods=['GET', 'POST'])
    # @login_required
    def contas_a_receber():
        from flask import render_template
        return render_template('contas_a_receber.html')
    
    @app.route('/contas_a_pagar')
    # @login_required
    def contas_a_pagar():
        from flask import render_template
        return render_template('contas_a_pagar.html')
    
    @app.route('/financeiro')
    # @login_required
    def financeiro():
        from flask import render_template
        return render_template('financeiro.html')
    
    @app.route('/faturamento')
    # @login_required
    def faturamento():
        from flask import render_template
        return render_template('faturamento.html')
    
    @app.route('/cotacoes')
    # @login_required
    def cotacoes():
        from flask import render_template
        return render_template('cotacoesfaturamento.html')
    
    @app.route('/nfvenda', methods=['GET', 'POST'])
    # @login_required
    def nfvenda():
        from flask import render_template, request, redirect, url_for, flash
        if request.method == 'POST':
            flash("Simulação: Dados da NF-e recebidos com sucesso! (Transmissão real pendente)", "info")
            return redirect(url_for('dashboard'))
        dados_emitente = {
            "cnpj": "00.000.000/0001-00",
            "nome_fantasia": "Minha Empresa LTDA",
            "ie": "123.456.789.000"
        }
        return render_template('nfvenda.html', dados_emitente=dados_emitente)
    
    @app.route('/nfse')
    # @login_required
    def nfse():
        from flask import render_template
        dados_emitente = {
            'cnpj': '00.000.000/0001-00',
            'razao_social': 'Sua Empresa de Serviços Ltda.',
            'inscricao_municipal': '4567890'
        }
        return render_template('nfse.html', dados_emitente=dados_emitente)

if __name__ == '__main__':
    app = create_app()
    
    # Criar tabelas se não existirem
    # Comentado temporariamente - precisa do PostgreSQL configurado
    # with app.app_context():
    #     db.create_all()
    
    app.run(debug=True)

