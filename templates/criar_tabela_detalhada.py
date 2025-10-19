import psycopg2
import sys

# Configurações de conexão com o banco de dados
DB_NAME = "sistema_login"
DB_USER = "postgres"
DB_PASSWORD = "postgres" # **ATENÇÃO: Mude para a sua senha real do PostgreSQL**
DB_HOST = "localhost"
DB_PORT = "5432"

def criar_tabela_detalhada():
    """
    Função que se conecta ao banco de dados e cria a tabela 'Pessoas'
    com todos os campos detalhados.
    """
    conn = None
    try:
        # Conectando ao banco de dados
        conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )
        cursor = conn.cursor()

        # Comando SQL para excluir a tabela antiga (se ela existir)
        # Isso garante que a nova tabela será criada corretamente
        drop_table_query = """
        DROP TABLE IF EXISTS Pessoas;
        """
        cursor.execute(drop_table_query)
        conn.commit()
        print("Tabela 'Pessoas' antiga excluída (se existia).")

        # Comando SQL para criar a nova tabela 'Pessoas' com todos os campos
        create_table_query = """
        CREATE TABLE Pessoas (
            id SERIAL PRIMARY KEY,
            nome_completo VARCHAR(255) NOT NULL,
            tipo VARCHAR(50) NOT NULL,
            
            -- Campos para Clientes
            cpf_cnpj VARCHAR(20) UNIQUE,
            data_nascimento DATE,
            informacoes_compra TEXT,
            
            -- Campos para Fornecedores e Vendedores
            endereco TEXT,
            telefone VARCHAR(50),
            email VARCHAR(255) UNIQUE,
            
            -- Campos Específicos para Fornecedores
            contatos_fornecedor TEXT,
            produtos_servicos TEXT,
            prazos_entrega TEXT,
            condicoes_pagamento TEXT,
            
            -- Campos Específicos para Vendedores
            cargo VARCHAR(100),
            comissoes DECIMAL(10, 2),
            
            data_cadastro TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
        );
        """
        
        # Executando o comando SQL para criar a nova tabela
        cursor.execute(create_table_query)
        conn.commit()

        print("Nova tabela 'Pessoas' com campos detalhados criada com sucesso.")

    except psycopg2.OperationalError as e:
        print(f"Erro de conexão com o banco de dados: {e}")
        print("Verifique se o banco de dados está rodando e se as suas credenciais estão corretas.")
        sys.exit(1)
    except Exception as e:
        print(f"Ocorreu um erro inesperado: {e}")
        sys.exit(1)
    finally:
        if conn:
            cursor.close()
            conn.close()
            print("Conexão com o banco de dados fechada.")

if __name__ == "__main__":
    criar_tabela_detalhada()
