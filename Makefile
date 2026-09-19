PYTHON = python
APP_DIR = backend
PORT = 8001

.PHONY: help run test clean compose-up compose-down compose-logs compose-ps compose-clean compose-shell compose-backend compose-db compose-test

help:
	@echo "Uso: make [alvo]"
	@echo ""
	@echo "Alvos Locais:"
	@echo "  help             - Exibe os comandos disponíveis"
	@echo "  run              - Executa a aplicação localmente com Poetry"
	@echo "  test             - Executa os testes unitários localmente"
	@echo "  clean            - Limpa arquivos temporários locais (__pycache__)"
	@echo ""
	@echo "Alvos Docker Compose:"
	@echo "  compose-up       - Constrói e sobe todos os serviços em segundo plano"
	@echo "  compose-down     - Para e remove todos os contêineres e redes"
	@echo "  compose-backend  - Sobe apenas o serviço de backend (e dependências)"
	@echo "  compose-db       - Sobe apenas o banco de dados PostgreSQL"
	@echo "  compose-logs     - Acompanha os logs dos contêineres em tempo real"
	@echo "  compose-ps       - Exibe o status e as portas dos contêineres"
	@echo "  compose-test     - Executa os testes unitários dentro do contêiner backend"
	@echo "  compose-shell    - Abre um terminal interativo no contêiner backend"
	@echo "  compose-clean    - Para os contêineres e remove volumes (reseta o banco)"

# --- Comandos Locais ---
run:
	@echo "Iniciando aplicação localmente..."
	cd $(APP_DIR) && poetry run uvicorn main:app --reload --port $(PORT)

test:
	@echo "Executando testes locais..."
	cd $(APP_DIR) && poetry run pytest

clean:
	@echo "Limpando arquivos temporários locais..."
	cd $(APP_DIR) && rm -rf __pycache__ tests/__pycache__
	cd $(APP_DIR) && rm -rf .pytest_cache .ruff_cache *.pyc *.pyd

# --- Comandos Docker Compose ---
compose-up:
	@echo "Subindo todos os serviços com Docker Compose..."
	docker compose up -d --build

compose-down:
	@echo "Parando todos os serviços..."
	docker compose down

compose-backend:
	@echo "Subindo o serviço de backend..."
	docker compose up -d --build backend

compose-db:
	@echo "Subindo apenas o banco de dados PostgreSQL..."
	docker compose up -d db

compose-logs:
	@echo "Exibindo logs dos contêineres..."
	docker compose logs -f

compose-ps:
	@echo "Status dos serviços:"
	docker compose ps

compose-test:
	@echo "Executando testes dentro do contêiner backend..."
	docker compose exec backend poetry run pytest

compose-shell:
	@echo "Acessando terminal do contêiner backend..."
	docker compose exec backend /bin/sh

compose-clean:
	@echo "Removendo contêineres, redes e volumes persistentes..."
	docker compose down -v