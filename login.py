import tkinter as tk
from tkinter import messagebox
import psycopg2
import bcrypt # Você precisa instalar esta biblioteca: pip install bcrypt

# IMPORTANTE: A senha no seu banco de dados precisa estar hasheada com bcrypt
def verificar_login():
    usuario = entry_usuario.get()
    senha = entry_senha.get().encode('utf-8')

    try:
        # Conexão com o banco de dados
        conexao = psycopg2.connect(
            dbname="sistema_login",
            user="postgres",
            password="postgres",
            host="localhost",
            port="5432"
        )
        cursor = conexao.cursor()

        # Consulta para obter o hash da senha do usuário
        cursor.execute("SELECT senha_hash FROM usuarios WHERE usuario=%s", (usuario,))
        resultado = cursor.fetchone()

        # ---- LÓGICA DE VERIFICAÇÃO ----
        if resultado:
            # Se a consulta retornou algo, o usuário existe
            senha_hash_banco = resultado[0].encode('utf-8')

            # Agora, verifique se a senha digitada corresponde ao hash do banco
            if bcrypt.checkpw(senha, senha_hash_banco):
                messagebox.showinfo("Login", "Login realizado com sucesso! ✅")
            else:
                # A senha digitada está incorreta
                messagebox.showerror("Login", "Usuário ou senha inválidos ❌")
        else:
            # Se a consulta retornou None, o usuário não existe no banco
            messagebox.showerror("Login", "Usuário ou senha inválidos ❌")

        conexao.close()

    except psycopg2.OperationalError as e:
        messagebox.showerror("Erro", f"Erro de conexão com o banco de dados: {e}")
    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro inesperado: {e}")

# Criar janela principal
janela = tk.Tk()
janela.title("Tela de Login")
janela.geometry("300x200")

# Label e campo de usuário
label_usuario = tk.Label(janela, text="Usuário:")
label_usuario.pack(pady=5)
entry_usuario = tk.Entry(janela)
entry_usuario.pack(pady=5)

# Label e campo de senha
label_senha = tk.Label(janela, text="Senha:")
label_senha.pack(pady=5)
entry_senha = tk.Entry(janela, show="*")
entry_senha.pack(pady=5)

# Botão de login
btn_login = tk.Button(janela, text="Entrar", command=verificar_login)
btn_login.pack(pady=20)

# Bind para permitir login com a tecla Enter
janela.bind('<Return>', lambda event: verificar_login())

# Executar janela
janela.mainloop()