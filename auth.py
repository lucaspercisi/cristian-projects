"""
Sistema de autenticação
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash
# Temporariamente comentado - precisa do banco configurado
# from flask_login import login_user, logout_user, login_required, current_user
# from models import db, User
# from config import config

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Página de login"""
    if request.method == 'POST':
        usuario = request.form.get('usuario')
        senha = request.form.get('senha')
        
        if not usuario or not senha:
            flash('Por favor, preencha todos os campos.', 'error')
            return render_template('login.html')
        
        # Login temporário simplificado - SEM VALIDAÇÃO REAL
        # Quando PostgreSQL estiver configurado, descomente abaixo
        # user = User.query.filter_by(usuario=usuario).first()
        # if user and user.check_password(senha):
        #     login_user(user, remember=True)
        #     flash(f'Bem-vindo, {user.usuario}!', 'success')
        #     return redirect(url_for('dashboard'))
        # else:
        #     flash('Usuário ou senha inválidos.', 'error')
        
        # Login temporário - aceita qualquer credencial
        flash(f'Login temporário: Bem-vindo, {usuario}! (Sem validação real ainda)', 'success')
        return redirect(url_for('dashboard'))
    
    return render_template('login.html')

@auth_bp.route('/logout')
# @login_required  # Temporariamente comentado
def logout():
    """Logout do usuário"""
    # logout_user()  # Temporariamente comentado
    flash('Logout realizado com sucesso!', 'info')
    return redirect(url_for('auth.login'))

@auth_bp.route('/perfil')
# @login_required  # Temporariamente comentado
def perfil():
    """Página de perfil do usuário"""
    return render_template('perfil.html')

def init_auth(app):
    """Inicializa o sistema de autenticação"""
    app.register_blueprint(auth_bp)

