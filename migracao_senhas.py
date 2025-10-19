import psycopg2
import bcrypt

# Configurações de conexão com o banco de dados
DB_NAME = "sistema_login"
DB_USER = "postgres"
DB_PASSWORD = "postgres" # **ATENÇÃO: Mude para a sua senha real do PostgreSQL**
DB_HOST = "localhost"
DB_PORT = "5432"

try:
    # Conectando ao banco de dados
    conexao = psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )
    cursor = conexao.cursor()

    print("Conexão com o banco de dados estabelecida com sucesso.")

    # 1. Seleciona todos os usuários e suas senhas antigas (em texto puro)
    #    A coluna "senha" deve existir na sua tabela para este passo.
    cursor.execute("SELECT usuario, senha FROM usuarios")
    usuarios = cursor.fetchall()

    if not usuarios:
        print("Nenhum usuário encontrado para migração.")
    else:
        print(f"{len(usuarios)} usuário(s) encontrado(s) para migrar.")

    # 2. Itera sobre cada usuário para hashear a senha
    for usuario, senha_texto_puro in usuarios:
        # Se a senha for NULL ou vazia, pula para o próximo usuário
        if not senha_texto_puro:
            print(f"Aviso: Senha em branco para o usuário '{usuario}'. Pulando...")
            continue

        # Codifica a senha em texto puro para bytes (necessário para o bcrypt)
        senha_bytes = senha_texto_puro.encode('utf-8')
        
        # Gera o hash com um novo "salt" aleatório
        senha_hash = bcrypt.hashpw(senha_bytes, bcrypt.gensalt())
        
        # Decodifica o hash para string (necessário para salvar no banco)
        senha_hash_string = senha_hash.decode('utf-8')

        # 3. Atualiza o banco com o novo hash na coluna 'senha_hash'
        cursor.execute("UPDATE usuarios SET senha_hash = %s WHERE usuario = %s", (senha_hash_string, usuario))
        
        print(f"Senha de '{usuario}' hasheada e atualizada com sucesso.")

    # 4. Confirma as mudanças no banco de dados
    conexao.commit()
    print("\nProcesso de migração concluído. As senhas foram hasheadas e salvas na coluna 'senha_hash'.")

except psycopg2.OperationalError as e:
    print(f"Erro de conexão com o banco de dados: {e}")
    print("Verifique se o banco de dados está rodando e se as suas credenciais de acesso estão corretas.")
except Exception as e:
    print(f"Ocorreu um erro inesperado: {e}")

finally:
    # Garante que a conexão seja fechada
    if 'conexao' in locals() and conexao:
        cursor.close()
        conexao.close()
        print("Conexão com o banco de dados fechada.")