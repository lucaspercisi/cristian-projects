#!/usr/bin/env bash
set -euo pipefail

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$PROJECT_DIR"

if [ ! -d ".venv" ]; then
    python -m venv .venv
fi

if [[ "${OSTYPE:-}" == msys* || "${OSTYPE:-}" == cygwin* || "${OSTYPE:-}" == "win32" ]]; then
    # Git Bash / MSYS2 / Cygwin no Windows
    source .venv/Scripts/activate
else
    source .venv/bin/activate
fi

pip install --upgrade pip
pip install -r requirements.txt

echo "Ambiente pronto. Configure as variáveis FLASK_APP e FLASK_ENV conforme necessário."
echo "Para iniciar o servidor Flask em modo debug, execute:"
echo "  flask run --debug"
