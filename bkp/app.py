from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3

app = Flask(__name__)
app.secret_key = 'sua_chave_secreta_aqui'  # Altere isso para uma chave secreta real

# Função para conectar ao banco de dados SQLite
def get_db_connection():
    conn = sqlite3.connect('banco_de_dados.db')
    conn.row_factory = sqlite3.Row
    return conn

# Rota para a página inicial (pode ser a mesma do dashboard)
@app.route('/')
def index():
    return redirect(url_for('dashboard'))

# Rota do Dashboard
@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

# Rota para a página de cadastro geral
@app.route('/cadastrar_geral', methods=['GET', 'POST'])
def cadastrar_geral():
    sucesso = None
    erro = None
    if request.method == 'POST':
        tipo = request.form.get('tipo')
        nome_completo = request.form.get('nome_completo')
        
        try:
            conn = get_db_connection()
            if tipo == 'cliente':
                cpf_cnpj = request.form.get('cpf_cnpj_cliente')
                data_nascimento = request.form.get('data_nascimento')
                informacoes_compra = request.form.get('informacoes_compra')
                
                conn.execute('INSERT INTO clientes (nome_completo, cpf_cnpj, data_nascimento, informacoes_compra) VALUES (?, ?, ?, ?)',
                             (nome_completo, cpf_cnpj, data_nascimento, informacoes_compra))
                
            elif tipo == 'fornecedor':
                cpf_cnpj = request.form.get('cpf_cnpj_fornecedor')
                endereco = request.form.get('endereco_forn')
                telefone = request.form.get('telefone_forn')
                email = request.form.get('email_forn')
                contatos_fornecedor = request.form.get('contatos_fornecedor')
                produtos_servicos = request.form.get('produtos_servicos')
                prazos_entrega = request.form.get('prazos_entrega')
                condicoes_pagamento = request.form.get('condicoes_pagamento')
                
                conn.execute('INSERT INTO fornecedores (nome_completo, cpf_cnpj, endereco, telefone, email, contatos_fornecedor, produtos_servicos, prazos_entrega, condicoes_pagamento) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)',
                             (nome_completo, cpf_cnpj, endereco, telefone, email, contatos_fornecedor, produtos_servicos, prazos_entrega, condicoes_pagamento))

            elif tipo == 'vendedor':
                cpf_cnpj = request.form.get('cpf_cnpj_vendedor')
                endereco = request.form.get('endereco_vend')
                telefone = request.form.get('telefone_vend')
                email = request.form.get('email_vend')
                cargo = request.form.get('cargo')
                comissoes = request.form.get('comissoes')
                
                conn.execute('INSERT INTO vendedores (nome_completo, cpf_cnpj, endereco, telefone, email, cargo, comissoes) VALUES (?, ?, ?, ?, ?, ?, ?)',
                             (nome_completo, cpf_cnpj, endereco, telefone, email, cargo, comissoes))

            conn.commit()
            sucesso = f'Cadastro de {tipo} realizado com sucesso!'
        except sqlite3.IntegrityError:
            erro = 'Erro: O CPF/CNPJ informado já existe.'
        except Exception as e:
            erro = f'Ocorreu um erro: {e}'
        finally:
            conn.close()

    return render_template('cadastro_geral.html', sucesso=sucesso, erro=erro)

# Rota para a página de cadastro de serviços
@app.route('/cadastrar_servicos', methods=['GET', 'POST'])
def cadastrar_servicos():
    # Lógica para lidar com o formulário de cadastro de serviços
    # ...
    return render_template('cadastro_servicos.html')

# Rota para a página de controle financeiro
@app.route('/financeiro')
def financeiro():
    # Lógica para buscar e exibir dados financeiros do banco de dados
    # ...
    return render_template('financeiro.html')

if __name__ == '__main__':
    app.run(debug=True)
