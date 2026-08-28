PYTHON = python
APP_DIR = backend
PORT = 8001

.PHONY: help run test clean

help:
	@echo "Uso: make [alvo]"
	@echo ""
	@echo "Alvos disponíveis:"
	@echo "  help   - Exibe os comandos disponíveis"
	@echo "  run    - Executa a aplicação"
	@echo "  test   - Executa os testes unitários"
	@echo "  clean  - Limpa arquivos temporários"

run:
	@echo "Iniciando aplicação..."
	cd $(APP_DIR) && poetry run uvicorn main:app --reload --port $(PORT)

test:
	@echo "Executando testes..."
	cd $(APP_DIR) && poetry run pytest

clean:
	@echo "Limpando arquivos temporários..."
	cd $(APP_DIR) && rm -rf __pycache__/ *.pyc *.pyd