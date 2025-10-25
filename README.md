# Guia de execução do projeto

Este repositório contém uma aplicação Flask que fornece dashboards e rotinas de cadastros, financeiro e logística consumindo um banco PostgreSQL chamado `sistema_login`. Também há scripts auxiliares para autenticação desktop (Tkinter) e migração/criação de tabelas.

## Dependências

As principais bibliotecas necessárias estão listadas em [`requirements.txt`](requirements.txt):

- `Flask` – framework web usado em `app.py`.
- `psycopg2-binary` – driver PostgreSQL utilizado nas rotas do Flask e scripts auxiliares.
- `bcrypt` – utilizado para gerar e validar hashes de senha nos scripts desktop/migração.

> **Observação:** o projeto não inclui o servidor PostgreSQL; instale-o separadamente (versão 14 ou superior recomendada).

## Preparando o banco de dados PostgreSQL

1. Instale o PostgreSQL e configure um usuário local com permissões para criar bancos e tabelas.
2. Crie o banco de dados `sistema_login` (ou ajuste o nome nos arquivos que consomem o banco).
3. Atualize as credenciais (usuário, senha, host) dentro dos scripts conforme o seu ambiente.
4. Execute `python criar_tabela_detalhada.py` para criar a tabela `Pessoas`.
5. Crie manualmente as demais tabelas utilizadas nas rotas do Flask (`produtos`, `contas_receber`, `contas_pagar`, `notas_fiscais_servico`, etc.). O SQL de cada rota em `app.py` pode servir como referência.
6. Se estiver migrando senhas legadas, execute `python migracao_senhas.py` após configurar as credenciais corretas.

## Preparação do ambiente no Windows + VSCode

1. Instale Python 3.10 ou superior, Git e VSCode (com as extensões "Python" e "Pylance").
2. Clone o repositório:
   ```bash
   git clone <url-do-repositorio>
   cd cristian-projects
   ```
3. Crie/atualize o arquivo [`requirements.txt`](requirements.txt) com as dependências acima (já incluso neste repositório).
4. Execute o script [`setup_and_run.sh`](setup_and_run.sh) em um terminal Git Bash para criar o ambiente virtual e instalar as dependências:
   ```bash
   chmod +x setup_and_run.sh
   ./setup_and_run.sh
   ```
5. No VSCode, abra a pasta do projeto e selecione o interpretador `.venv` (Ctrl + Shift + P → "Python: Select Interpreter").
6. Defina as variáveis de ambiente do Flask (ajuste conforme seu terminal):
   - PowerShell:
     ```powershell
     setx FLASK_APP "app.py"
     setx FLASK_ENV "development"
     ```
   - Git Bash (válido apenas na sessão atual):
     ```bash
     export FLASK_APP=app.py
     export FLASK_ENV=development
     ```
7. Inicie o servidor Flask (garanta que o PostgreSQL está em execução):
   ```bash
   flask run --debug
   ```
   A aplicação ficará disponível em `http://127.0.0.1:5000/`.

## Executando o aplicativo desktop (opcional)

Para utilizar o login via Tkinter:

```bash
python login.py
```

Esse script utiliza as mesmas credenciais PostgreSQL e depende do Tkinter instalado junto com o Python.

## Problemas conhecidos e recomendações

- As credenciais do banco estão hardcoded nos arquivos. Recomenda-se trocá-las por variáveis de ambiente.
- Algumas rotas dependem de tabelas que não possuem scripts de criação. Crie-as manualmente antes de rodar o sistema.
- O template `contas_a_receber.html` faz uma chamada para `/buscar_cliente`, rota que ainda não existe; ajuste a rota ou o JavaScript conforme necessário.
- Há código legado para SQLite (`iniciar_banco_sqlite.py`) que não faz parte do fluxo do Flask atual.

Sinta-se à vontade para adaptar este guia às necessidades específicas do seu ambiente.
