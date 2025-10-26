"""
Modelos SQLAlchemy para a aplicação
"""
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime
import bcrypt

db = SQLAlchemy()

class User(UserMixin, db.Model):
    """Modelo de Usuário"""
    __tablename__ = 'usuarios'
    
    id = db.Column(db.Integer, primary_key=True)
    usuario = db.Column(db.String(80), unique=True, nullable=False)
    senha_hash = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=True)
    ativo = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime, nullable=True)
    
    # Relacionamentos
    perfil = db.relationship('PerfilUsuario', backref='usuario', uselist=False)
    permissoes = db.relationship('Permissao', secondary='usuario_permissoes', back_populates='usuarios')
    
    def set_password(self, password):
        """Gera hash da senha"""
        self.senha_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    def check_password(self, password):
        """Verifica se a senha está correta"""
        return bcrypt.checkpw(password.encode('utf-8'), self.senha_hash.encode('utf-8'))
    
    def __repr__(self):
        return f'<User {self.usuario}>'

class PerfilUsuario(db.Model):
    """Perfil do usuário"""
    __tablename__ = 'perfil_usuario'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), unique=True)
    nome_completo = db.Column(db.String(200))
    telefone = db.Column(db.String(20))
    cargo = db.Column(db.String(100))
    departamento = db.Column(db.String(100))
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Permissao(db.Model):
    """Permissões do sistema"""
    __tablename__ = 'permissoes'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(80), unique=True, nullable=False)
    descricao = db.Column(db.String(255))
    usuarios = db.relationship('User', secondary='usuario_permissoes', back_populates='permissoes')
    
    def __repr__(self):
        return f'<Permissao {self.nome}>'

# Tabela de associação para usuário-permissões
usuario_permissoes = db.Table('usuario_permissoes',
    db.Column('user_id', db.Integer, db.ForeignKey('usuarios.id'), primary_key=True),
    db.Column('permissoes_id', db.Integer, db.ForeignKey('permissoes.id'), primary_key=True)
)

class Pessoa(db.Model):
    """Cadastro Geral de Pessoas (Clientes, Fornecedores, etc)"""
    __tablename__ = 'pessoas'
    
    codigo_cadastro = db.Column(db.Integer, primary_key=True)
    tipo = db.Column(db.String(50))  # cliente, fornecedor, vendedor, etc
    tipo_classificacao = db.Column(db.String(50))
    cpf_cnpj = db.Column(db.String(20))
    nome_completo = db.Column(db.String(200))
    razao_social = db.Column(db.String(200))
    nome_fantasia = db.Column(db.String(200))
    contribuinte = db.Column(db.String(50))
    logradouro = db.Column(db.String(200))
    numero = db.Column(db.String(20))
    letra = db.Column(db.String(10))
    complemento = db.Column(db.String(100))
    bairro = db.Column(db.String(100))
    cidade = db.Column(db.String(100))
    cep = db.Column(db.String(20))
    nome_contato = db.Column(db.String(200))
    telefone_fixo = db.Column(db.String(20))
    telefone_celular = db.Column(db.String(20))
    email = db.Column(db.String(200))
    cargo = db.Column(db.String(100))
    comissoes = db.Column(db.Numeric(10, 2))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<Pessoa {self.nome_completo or self.razao_social}>'

class Produto(db.Model):
    """Cadastro de Produtos"""
    __tablename__ = 'produtos'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(200), nullable=False)
    codigo_barras = db.Column(db.String(50))
    codigo_exportacao = db.Column(db.String(50))
    codigo_importacao = db.Column(db.String(50))
    origem_internacional = db.Column(db.Boolean, default=False)
    descricao = db.Column(db.Text)
    preco_custo = db.Column(db.Numeric(10, 2))
    preco_venda = db.Column(db.Numeric(10, 2))
    quantidade_estoque = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<Produto {self.nome}>'

class ContaReceber(db.Model):
    """Contas a Receber"""
    __tablename__ = 'contas_receber'
    
    codigo_lancamento = db.Column(db.Integer, primary_key=True)
    codigo_cliente = db.Column(db.Integer, db.ForeignKey('pessoas.codigo_cadastro'))
    numero_documento = db.Column(db.String(50))
    chave_nfe = db.Column(db.String(100))
    data_emissao = db.Column(db.Date)
    valor_total = db.Column(db.Numeric(10, 2))
    condicao_recebimento = db.Column(db.String(100))
    forma_recebimento = db.Column(db.String(100))
    observacoes = db.Column(db.Text)
    status = db.Column(db.String(20), default='pendente')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    cliente = db.relationship('Pessoa', foreign_keys=[codigo_cliente])
    
    def __repr__(self):
        return f'<ContaReceber {self.numero_documento}>'

class ContaPagar(db.Model):
    """Contas a Pagar"""
    __tablename__ = 'contas_pagar'
    
    codigo_lancamento = db.Column(db.Integer, primary_key=True)
    codigo_fornecedor = db.Column(db.Integer, db.ForeignKey('pessoas.codigo_cadastro'))
    numero_documento = db.Column(db.String(50))
    data_vencimento = db.Column(db.Date)
    valor_total = db.Column(db.Numeric(10, 2))
    forma_pagamento = db.Column(db.String(100))
    observacoes = db.Column(db.Text)
    status = db.Column(db.String(20), default='pendente')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    fornecedor = db.relationship('Pessoa', foreign_keys=[codigo_fornecedor])
    
    def __repr__(self):
        return f'<ContaPagar {self.numero_documento}>'

