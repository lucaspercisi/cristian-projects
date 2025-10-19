import sqlite3

def iniciar_banco_de_dados():
    try:
        conn = sqlite3.connect('banco_de_dados.db')
        cursor = conn.cursor()

        # Cria a tabela de clientes
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS clientes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tipo_classificacao TEXT NOT NULL,
                cpf_cnpj TEXT NOT NULL UNIQUE,
                nome_completo TEXT,
                razao_social TEXT,
                nome_fantasia TEXT,
                contribuinte TEXT,
                logradouro TEXT,
                numero TEXT,
                letra TEXT,
                complemento TEXT,
                bairro TEXT,
                cidade TEXT,
                cep TEXT,
                nome_contato TEXT,
                telefone_fixo TEXT,
                telefone_celular TEXT,
                email TEXT
            );
        ''')

        # Cria a tabela de fornecedores
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS fornecedores (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tipo_classificacao TEXT NOT NULL,
                cpf_cnpj TEXT NOT NULL UNIQUE,
                nome_completo TEXT,
                razao_social TEXT,
                nome_fantasia TEXT,
                contribuinte TEXT,
                logradouro TEXT,
                numero TEXT,
                letra TEXT,
                complemento TEXT,
                bairro TEXT,
                cidade TEXT,
                cep TEXT,
                nome_contato TEXT,
                telefone_fixo TEXT,
                telefone_celular TEXT,
                email TEXT
            );
        ''')
        
        # Cria a tabela de vendedores
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS vendedores (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tipo_classificacao TEXT NOT NULL,
                cpf_cnpj TEXT NOT NULL UNIQUE,
                nome_completo TEXT,
                razao_social TEXT,
                nome_fantasia TEXT,
                contribuinte TEXT,
                logradouro TEXT,
                numero TEXT,
                letra TEXT,
                complemento TEXT,
                bairro TEXT,
                cidade TEXT,
                cep TEXT,
                nome_contato TEXT,
                telefone_fixo TEXT,
                telefone_celular TEXT,
                email TEXT,
                cargo TEXT,
                comissoes REAL
            );
        ''')
        
        conn.commit()
        print("Tabelas 'clientes', 'fornecedores' e 'vendedores' criadas com sucesso no banco de dados SQLite.")
        
    except sqlite3.Error as e:
        print(f"Erro ao criar as tabelas: {e}")
    finally:
        if 'conn' in locals() and conn:
            conn.close()

if __name__ == '__main__':
    iniciar_banco_de_dados()