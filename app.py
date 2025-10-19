from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import psycopg2
import psycopg2.extras
from datetime import date
from flask import Flask, render_template, request, redirect, url_for, flash


app = Flask(__name__)
app.secret_key = 'sua_chave_secreta_aqui'

# ----------------------------
# Conexão com PostgreSQL
# ----------------------------
def get_pg_connection():
    try:
        conn = psycopg2.connect(
            dbname="sistema_login",
            user="postgres",
            password="postgres",
            host="localhost",
            port="5432"
        )
        return conn
    except psycopg2.OperationalError as e:
        print(f"Erro ao conectar ao PostgreSQL: {e}")
        return None

# ----------------------------
# Rotas principais
# ----------------------------
@app.route('/')
def index():
    return redirect(url_for('dashboard'))

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

# ----------------------------
# Cadastro Geral (Pessoas)
# ----------------------------
@app.route('/cadastrar_geral', methods=['GET', 'POST'])
def cadastrar_geral():
    sucesso = None
    erro = None
    proximo_codigo = 1

    conn = get_pg_connection()
    if not conn:
        erro = "Erro: Não foi possível conectar ao banco de dados."
        return render_template('cadastro_geral.html', sucesso=sucesso, erro=erro, proximo_codigo=proximo_codigo)

    try:
        with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
            if request.method == 'POST':
                codigo_cadastro = request.form.get('codigo_cadastro')
                tipo = request.form.get('tipo')
                tipo_classificacao = request.form.get('tipo_classificacao')
                cpf_cnpj = request.form.get('cpf_cnpj')
                nome_completo = request.form.get('nome_completo')
                razao_social = request.form.get('razao_social')
                nome_fantasia = request.form.get('nome_fantasia')
                contribuinte = request.form.get('contribuinte')
                logradouro = request.form.get('logradouro')
                numero = request.form.get('numero')
                letra = request.form.get('letra')
                complemento = request.form.get('complemento')
                bairro = request.form.get('bairro')
                cidade = request.form.get('cidade')
                cep = request.form.get('cep')
                nome_contato = request.form.get('nome_contato')
                telefone_fixo = request.form.get('telefone_fixo')
                telefone_celular = request.form.get('telefone_celular')
                email = request.form.get('email')
                cargo = request.form.get('cargo')
                comissoes = request.form.get('comissoes') if request.form.get('comissoes') else None

                cursor.execute("SELECT * FROM pessoas WHERE codigo_cadastro = %s", (codigo_cadastro,))
                existe = cursor.fetchone()

                if existe:
                    query = """
                        UPDATE pessoas SET tipo=%s, tipo_classificacao=%s, cpf_cnpj=%s, nome_completo=%s, 
                        razao_social=%s, nome_fantasia=%s, contribuinte=%s, logradouro=%s, numero=%s, 
                        letra=%s, complemento=%s, bairro=%s, cidade=%s, cep=%s, nome_contato=%s, 
                        telefone_fixo=%s, telefone_celular=%s, email=%s, cargo=%s, comissoes=%s
                        WHERE codigo_cadastro = %s
                    """
                    cursor.execute(query, (tipo, tipo_classificacao, cpf_cnpj, nome_completo, razao_social, 
                                           nome_fantasia, contribuinte, logradouro, numero, letra, complemento, 
                                           bairro, cidade, cep, nome_contato, telefone_fixo, telefone_celular, 
                                           email, cargo, comissoes, codigo_cadastro))
                    sucesso = "Cadastro atualizado com sucesso!"
                else:
                    query = """
                        INSERT INTO pessoas (codigo_cadastro, tipo, tipo_classificacao, cpf_cnpj, nome_completo, 
                        razao_social, nome_fantasia, contribuinte, logradouro, numero, letra, complemento, 
                        bairro, cidade, cep, nome_contato, telefone_fixo, telefone_celular, email, cargo, comissoes)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """
                    cursor.execute(query, (codigo_cadastro, tipo, tipo_classificacao, cpf_cnpj, nome_completo, 
                                           razao_social, nome_fantasia, contribuinte, logradouro, numero, letra, 
                                           complemento, bairro, cidade, cep, nome_contato, telefone_fixo, 
                                           telefone_celular, email, cargo, comissoes))
                    sucesso = "Pessoa cadastrada com sucesso!"
                conn.commit()

            # calcula próximo código
            cursor.execute("SELECT MAX(codigo_cadastro) FROM pessoas")
            max_id_result = cursor.fetchone()
            max_id = max_id_result[0] if max_id_result and max_id_result[0] else 0
            proximo_codigo = int(max_id) + 1

    except psycopg2.Error as e:
        conn.rollback()
        erro = f"Erro no banco de dados: {e}"
    finally:
        conn.close()

    return render_template('cadastro_geral.html', sucesso=sucesso, erro=erro, proximo_codigo=proximo_codigo)

# ----------------------------
# Cadastro de Produtos
# ----------------------------
@app.route('/cadastrar_produtos', methods=['GET', 'POST'])
def cadastrar_produtos():
    sucesso = None
    erro = None
    conn = get_pg_connection()
    if not conn:
        erro = "Erro: Não foi possível conectar ao banco de dados."
        return render_template('cadastro_produtos.html', sucesso=sucesso, erro=erro)

    if request.method == 'POST':
        try:
            with conn.cursor() as cursor:
                nome = request.form['nome']
                codigo_barras = request.form.get('codigo_barras')
                codigo_exportacao = request.form.get('codigo_exportacao')
                codigo_importacao = request.form.get('codigo_importacao')
                origem_internacional = 'origem_internacional' in request.form
                descricao = request.form.get('descricao')

                preco_custo = request.form.get('preco_custo') or None
                preco_venda = request.form.get('preco_venda') or None
                quantidade_estoque = request.form.get('quantidade_estoque') or 0

                preco_custo = float(preco_custo) if preco_custo else None
                preco_venda = float(preco_venda) if preco_venda else None
                quantidade_estoque = int(quantidade_estoque) if quantidade_estoque else 0

                query = """
                    INSERT INTO produtos (nome, codigo_barras, codigo_exportacao, codigo_importacao, 
                    origem_internacional, descricao, preco_custo, preco_venda, quantidade_estoque)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                cursor.execute(query, (nome, codigo_barras, codigo_exportacao, codigo_importacao, 
                                       origem_internacional, descricao, preco_custo, preco_venda, quantidade_estoque))
                conn.commit()
                sucesso = "Produto cadastrado com sucesso!"
        except (psycopg2.Error, ValueError) as e:
            conn.rollback()
            erro = f"Erro: {e}"
        finally:
            conn.close()

    return render_template('cadastro_produtos.html', sucesso=sucesso, erro=erro)

# ----------------------------
# Cadastro de Serviços
# ----------------------------
@app.route('/cadastrar_servicos', methods=['GET', 'POST'])
def cadastrar_servicos():
    return render_template('cadastro_servicos.html')

# ----------------------------
# Financeiro
# ----------------------------
@app.route('/contas_a_receber', methods=['GET', 'POST'])
def contas_a_receber():
    sucesso = None
    erro = None
    conn = get_pg_connection()

    if not conn:
        erro = "Erro: Não foi possível conectar ao banco de dados."
        return render_template('contas_a_receber.html', sucesso=sucesso, erro=erro)

    if request.method == 'POST':
        try:
            with conn.cursor() as cursor:
                codigo_lancamento = request.form.get('codigo_lancamento') or None
                codigo_cliente = request.form.get('codigo_cliente') or None
                numero_documento = request.form.get('numero_documento') or None
                chave_nfe = request.form.get('chave_nfe') or None
                data_emissao = request.form.get('data_emissao') or None
                valor_total = request.form.get('valor_total') or None
                condicao_recebimento = request.form.get('condicao_recebimento') or None
                forma_recebimento = request.form.get('forma_recebimento') or None
                observacoes = request.form.get('observacoes') or None

                if codigo_lancamento:
                    # Atualiza lançamento existente
                    query = """
                        UPDATE contas_receber
                        SET codigo_cliente=%s, numero_documento=%s, chave_nfe=%s,
                            data_emissao=%s, valor_total=%s, condicao_recebimento=%s,
                            forma_recebimento=%s, observacoes=%s
                        WHERE codigo_lancamento=%s
                    """
                    cursor.execute(query, (codigo_cliente, numero_documento, chave_nfe,
                                           data_emissao, valor_total, condicao_recebimento,
                                           forma_recebimento, observacoes, codigo_lancamento))
                    sucesso = "Lançamento atualizado com sucesso!"
                else:
                    # Insere novo lançamento
                    query = """
                        INSERT INTO contas_receber
                        (codigo_cliente, numero_documento, chave_nfe, data_emissao,
                         valor_total, condicao_recebimento, forma_recebimento, observacoes)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                    """
                    cursor.execute(query, (codigo_cliente, numero_documento, chave_nfe,
                                           data_emissao, valor_total, condicao_recebimento,
                                           forma_recebimento, observacoes))
                    sucesso = "Lançamento cadastrado com sucesso!"

                conn.commit()
        except (psycopg2.Error, ValueError) as e:
            conn.rollback()
            erro = f"Erro no banco de dados: {e}"
        finally:
            conn.close()

    return render_template('contas_a_receber.html', sucesso=sucesso, erro=erro)



@app.route('/contas_a_pagar')
def contas_a_pagar():
    return render_template('contas_a_pagar.html')

@app.route('/financeiro')
def financeiro():
    return render_template('financeiro.html')

# ----------------------------
# Login / Perfil
# ----------------------------
from flask import request, render_template, redirect, url_for

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Lógica para processar o formulário de login
        usuario = request.form['usuario']
        senha = request.form['senha']
        # Verificação de credenciais aqui
        if usuario == 'admin' and senha == '1234':
            return redirect(url_for('dashboard'))
        else:
            return "Credenciais inválidas"
    # Se o método for GET, renderiza a página de login
    return render_template('login.html')

@app.route('/perfil')
def perfil():
    return render_template('perfil.html')

@app.route('/logout')
def logout():
    flash("Logout realizado com sucesso!", "info")
    return redirect(url_for('login'))

# ----------------------------
# APIs auxiliares (usadas no JS dos templates)
# ----------------------------
@app.route('/buscar_cadastro')
def buscar_cadastro():
    codigo = request.args.get('codigo')
    if not codigo:
        return jsonify({'encontrado': False})
    conn = get_pg_connection()
    if not conn:
        return jsonify({'encontrado': False, 'erro': 'Sem conexão'})
    try:
        with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
            cur.execute("SELECT * FROM pessoas WHERE codigo_cadastro = %s", (codigo,))
            row = cur.fetchone()
            if not row:
                return jsonify({'encontrado': False})
            return jsonify({'encontrado': True, 'cadastro': dict(row)})
    finally:
        conn.close()

@app.route('/buscar_fornecedor')
def buscar_fornecedor():
    codigo = request.args.get('codigo')
    if not codigo:
        return jsonify({'encontrado': False})
    conn = get_pg_connection()
    if not conn:
        return jsonify({'encontrado': False, 'erro': 'Sem conexão'})
    try:
        with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
            cur.execute("SELECT nome_completo AS nome FROM pessoas WHERE codigo_cadastro = %s AND tipo = 'fornecedor'", (codigo,))
            row = cur.fetchone()
            if not row:
                return jsonify({'encontrado': False})
            return jsonify({'encontrado': True, 'nome': row['nome']})
    finally:
        conn.close()

@app.route('/buscar_conta_a_pagar')
def buscar_conta_a_pagar():
    codigo = request.args.get('codigo')
    if not codigo:
        return jsonify({'encontrado': False})
    conn = get_pg_connection()
    if not conn:
        return jsonify({'encontrado': False, 'erro': 'Sem conexão'})
    try:
        with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
            cur.execute("SELECT * FROM contas_pagar WHERE codigo_lancamento = %s", (codigo,))
            row = cur.fetchone()
            if not row:
                return jsonify({'encontrado': False})
            return jsonify({'encontrado': True, 'lancamento': dict(row)})
    finally:
        conn.close()


@app.route('/buscar_conta_a_receber')
def buscar_conta_a_receber():
    codigo = request.args.get('codigo')
    if not codigo:
        return jsonify({'encontrado': False})
    conn = get_pg_connection()
    if not conn:
        return jsonify({'encontrado': False, 'erro': 'Sem conexão'})
    try:
        with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
            cur.execute("SELECT * FROM contas_receber WHERE codigo_lancamento = %s", (codigo,))
            row = cur.fetchone()
            if not row:
                return jsonify({'encontrado': False})
            return jsonify({'encontrado': True, 'lancamento': dict(row)})
    finally:
        conn.close()

# Adicione a rota para a nova página de cotações
@app.route('/faturamento')
def faturamento():
    return render_template('faturamento.html')


# Adicione a rota para a nova página de cotações
@app.route('/cotacoes')
def cotacoes():
    return render_template('cotacoesfaturamento.html')

# Rota para a tela de Documentação de Fluxo
@app.route('/documentacao')
def documentacao():
    return render_template('documentacaofluxo.html')


# ... outras configurações ...

@app.route('/nfvenda', methods=['GET', 'POST'])
def nfvenda():
    if request.method == 'POST':
        # Aqui você vai processar os dados do formulário
        # 1. Coletar os dados do request.form
        # 2. Validar os dados (essencial!)
        # 3. Gerar o XML da NF-e
        # 4. Assinar o XML
        # 5. Transmitir para a SEFAZ
        # 6. Tratar o retorno da SEFAZ (sucesso/erro)
        # 7. Salvar a nota fiscal no banco de dados (se autorizada)
        # 8. Redirecionar para uma página de sucesso ou exibir erros

        # Exemplo simples de coleta e retorno de dados (sem lógica de transmissão)
        dados_nf = {
            "emitente_cnpj": request.form.get('emitente_cnpj'),
            "destinatario_cnpj_cpf": request.form.get('destinatario_cnpj_cpf'),
            "destinatario_nome_razao": request.form.get('destinatario_nome_razao'),
            "destinatario_logradouro": request.form.get('destinatario_logradouro'),
            # ... outros campos ...
            "itens": []
        }

        # Coleta os itens adicionados
        for i in range(len(request.form.getlist('item_nome[]'))):
            dados_nf["itens"].append({
                "nome": request.form.getlist('item_nome[]')[i],
                "codigo": request.form.getlist('item_codigo[]')[i],
                "quantidade": request.form.getlist('item_quantidade[]')[i],
                "valor_unitario": request.form.getlist('item_valor_unitario[]')[i]
            })

        print("Dados coletados da NF-e:", dados_nf) # Para debug

        # Em um sistema real, você chamaria funções para gerar/transmitir o XML aqui.
        # Por enquanto, vamos apenas redirecionar para uma página fictícia ou flash uma mensagem.
        flash("Simulação: Dados da NF-e recebidos com sucesso! (Transmissão real pendente)", "info")
        return redirect(url_for('dashboard')) # Ou uma página de confirmação de NF-e

    # Se for GET, apenas renderiza o formulário
    # Você pode carregar dados do emitente do seu banco de dados aqui
    dados_emitente = {
        "cnpj": "00.000.000/0001-00",
        "nome_fantasia": "Minha Empresa LTDA",
        "ie": "123.456.789.000"
    }
    return render_template('nfvenda.html', dados_emitente=dados_emitente)

# Certifique-se de que 'emitir_nfvenda' no url_for('/nfvenda') corresponda ao nome da função aqui.
# Se o seu backend usa outra convenção, ajuste conforme necessário.


# Supondo que você tenha uma função para buscar os dados da sua empresa (emitente)
def get_dados_emitente():
    # Implemente a lógica para buscar os dados da sua empresa do banco de dados
    # Exemplo:
    return {
        'cnpj': '00.000.000/0001-00',
        'razao_social': 'Sua Empresa de Serviços Ltda.',
        'inscricao_municipal': '4567890'
    }

@app.route('/nfse')
def nfse():
    dados_emitente = get_dados_emitente()
    return render_template('nfse.html', dados_emitente=dados_emitente)

@app.route('/emitir_nfse', methods=['POST'])
def emitir_nfse():
    if request.method == 'POST':
        # Obter os dados do formulário
        prestador_cnpj = request.form.get('prestador_cnpj')
        prestador_nome = request.form.get('prestador_nome')
        prestador_im = request.form.get('prestador_inscricao_municipal')
        tomador_cpf_cnpj = request.form.get('tomador_cpf_cnpj')
        tomador_nome_razao = request.form.get('tomador_nome_razao')
        tomador_im = request.form.get('tomador_inscricao_municipal')
        tomador_email = request.form.get('tomador_email')
        servico_descricao = request.form.get('servico_descricao')
        codigo_servico = request.form.get('codigo_servico')
        cnae = request.form.get('cnae')
        valor_servicos = float(request.form.get('valor_servicos', 0.0))
        iss_aliquota = float(request.form.get('iss_aliquota', 0.0))
        deducoes = float(request.form.get('deducoes', 0.0))
        iss_valor = float(request.form.get('iss_valor', 0.0)) # Pode vir calculado do JS ou ser recalculado aqui
        valor_total_nfse = float(request.form.get('valor_total_nfse', 0.0)) # Pode vir calculado do JS ou ser recalculado aqui
        data_competencia = request.form.get('data_competencia')
        regime_tributario = request.form.get('regime_tributario')
        iss_retido = request.form.get('iss_retido') == 'true' # Converte string para boolean
        iss_retido_cnpj = request.form.get('iss_retido_cnpj')
        iss_retido_im = request.form.get('iss_retido_im')
        observacoes = request.form.get('observacoes')
        anexos = request.form.get('anexos') # Apenas o nome do arquivo neste exemplo

        # --- Validação dos dados ---
        # Adicione validações mais robustas aqui!
        if not tomador_cpf_cnpj or not servico_descricao or not codigo_servico or not valor_servicos or not data_competencia:
            flash("Por favor, preencha todos os campos obrigatórios.", "error")
            dados_emitente = get_dados_emitente()
            return render_template('nfse.html', dados_emitente=dados_emitente, erro="Campos obrigatórios não preenchidos.")

        # --- Lógica de Cálculo do ISS (pode ser feita no backend também) ---
        # Recalcular o ISS e Valor Total para garantir integridade
        base_calculo_iss = valor_servicos - deducoes
        valor_iss_calculado = base_calculo_iss * (iss_aliquota / 100)
        valor_total_nfse_calculado = valor_servicos - valor_iss_calculado - deducoes # ISS pode ser retido ou não, mas a base para valor total é esta

        # Se ISS for retido, o valor total pago pelo cliente é valor_servicos - valor_iss_calculado - deducoes
        # Se ISS não for retido, o valor total pago pelo cliente é valor_servicos - deducoes (e o ISS é pago separadamente)
        # A forma como o "Valor Total NFS-e" é exibido e pago pode variar dependendo da legislação e sistema.
        # Para simplificar, vou considerar o valor do serviço líquido de ISS e deduções como valor total da nota.

        # --- Lógica para Transmissão da NFS-e ---
        # Aqui você integraria com a API do seu município ou da prefeitura.
        # Esta parte é complexa e específica para cada cidade/estado.
        # Você precisaria:
        # 1. Obter um certificado digital (se necessário).
        # 2. Formatar os dados no padrão exigido pela prefeitura (XML, JSON, etc.).
        # 3. Enviar os dados para a API de homologação (teste) ou produção.
        # 4. Tratar as respostas da API (sucesso, erro, número da nota gerada).

        # Simulando uma emissão bem-sucedida:
        numero_nfse_gerada = "12345" # Simulado
        try:
            # Exemplo de como salvar os dados no banco (você precisará adaptar sua tabela de notas fiscais de serviço)
            conn = get_pg_connection()
            if conn:
                cursor = conn.cursor()
                # Assumindo que você tem uma tabela 'notas_fiscais_servico'
                query = """
                INSERT INTO notas_fiscais_servico (
                    prestador_cnpj, prestador_nome, prestador_im,
                    tomador_cpf_cnpj, tomador_nome_razao, tomador_im, tomador_email,
                    servico_descricao, codigo_servico, cnae, valor_servicos, iss_aliquota, deducoes, iss_valor, valor_total_nfse,
                    data_competencia, regime_tributario, iss_retido, iss_retido_cnpj, iss_retido_im,
                    observacoes, anexos, numero_nfse, status
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                cursor.execute(query, (
                    prestador_cnpj, prestador_nome, prestador_im,
                    tomador_cpf_cnpj, tomador_nome_razao, tomador_im, tomador_email,
                    servico_descricao, codigo_servico, cnae, valor_servicos, iss_aliquota, deducoes, valor_iss_calculado, valor_total_nfse_calculado,
                    data_competencia, regime_tributario, iss_retido, iss_retido_cnpj if iss_retido else None, iss_retido_im if iss_retido else None,
                    observacoes, anexos, numero_nfse_gerada, 'Emitida'
                ))
                conn.commit()
                cursor.close()
                conn.close()

                flash(f"NFS-e número {numero_nfse_gerada} emitida com sucesso!", "success")
                return redirect(url_for('nfse')) # Redireciona de volta para a página de emissão ou para uma página de consulta

            else:
                flash("Erro ao conectar ao banco de dados para salvar a NFS-e.", "error")
                return render_template('nfse.html', dados_emitente=get_dados_emitente(), erro="Erro ao salvar no banco.")

        except Exception as e:
            flash(f"Ocorreu um erro ao emitir a NFS-e: {e}", "error")
            # Em caso de erro na emissão ou cálculo, renderiza de volta com os dados preenchidos
            dados_emitente = get_dados_emitente()
            return render_template('nfse.html', dados_emitente=dados_emitente, erro=str(e))

    # Se não for POST (ex: GET para carregar o formulário)
    dados_emitente = get_dados_emitente()
    return render_template('nfse.html', dados_emitente=dados_emitente)


# Rota para a tela de Monitoramento Logístico
@app.route('/contrato')
def contrato():
    return render_template('contrato.html')


# Rota para a tela de Monitoramento Logístico
@app.route('/monitoramento')
def monitoramento():
    return render_template('monitoramento.html')

# Rota para a tela de Cadastro de Itens
@app.route('/lista_descricao_produtos_para_registro_di')
def lista_descricao_produtos_para_registro_di():
    return render_template('lista_descricao_produtos_para_registro_di.html')


# Rota para a tela de Controle de Processo
@app.route('/controle_processo')
def controle_processo():
    return render_template('ControleProcesso.html')


# Rota para a tela de Controle de Processo
@app.route('/servico_logistico')
def servico_logistico():
    return render_template('servico_logistico.html')

# --- Novas Rotas para Serviços Logísticos ---    <!-- Planilha APAxxx Controle processo -->



@app.route('/check_list_processos_apacomex')
def check_list_processos_apacomex():
    return render_template('check_list_processos_apacomex.html')


@app.route('/check_list_processos')
def check_list_processos():
    return render_template('check_list_processos.html')

@app.route('/cotacao_frete_internacional_rodoviario')
def cotacao_frete_internacional_rodoviario():
    return render_template('cotacao_frete_internacional_rodoviario.html')

@app.route('/analise_fechamento_frete')
def analise_fechamento_frete():
    return render_template('analise_fechamento_frete.html')

@app.route('/solicitacao_estimativa_custos')
def solicitacao_estimativa_custos():
    return render_template('solicitacao_estimativa_custos.html')

@app.route('/abertura_mex')
def abertura_mex():
    return render_template('abertura_mex.html')

@app.route('/lista_descricao_ncm')
def lista_descricao_ncm():
    return render_template('lista_descricao_ncm.html')

@app.route('/follow_up')
def follow_up():
    return render_template('follow_up.html')










@app.route('/assessoria_importacao_exportacao')
def assessoria_importacao_exportacao():
    return render_template('assessoria_importacao_exportacao.html')

@app.route('/processo_documental')
def processo_documental():
    # O erro anterior sugeriu 'documentacao', então vamos usar essa rota.
    # Se você já tem uma rota para 'documentacao', pode usar ela aqui.
    return redirect(url_for('documentacao'))

# @app.route('/contratacao_frete')
# def contratacao_frete():
#     return render_template('contratacao_frete.html')

@app.route('/despacho_aduaneiro')
def despacho_aduaneiro():
    return render_template('despacho_aduaneiro.html')

@app.route('/assessoria_cambial')
def assessoria_cambial():
    return render_template('assessoria_cambial.html')

@app.route('/habilitacoes_certificacoes')
def habilitacoes_certificacoes():
    return render_template('habilitacoes_certificacoes.html')

@app.route('/desenvolvimento_fornecedores')
def desenvolvimento_fornecedores():
    return render_template('desenvolvimento_fornecedores.html')


@app.route('/cotacao_cambio')
def cotacao_cambio():
    return render_template('cotacao_cambio.html')




# ----------------------------
# Main
# ----------------------------
if __name__ == "__main__":
    app.run(debug=True)
