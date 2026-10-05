PYTHON = python
APP_DIR = backend
PORT = 8001

.PHONY: help run test test-unit test-integration clean compose-up compose-down compose-logs compose-ps compose-clean compose-shell compose-backend compose-db compose-test

help:
	@echo "Uso: make [alvo]"
	@echo ""
	@echo "Alvos Locais:"
	@echo "  help             - Exibe os comandos disponíveis"
	@echo "  run              - Executa a aplicação localmente com Poetry"
	@echo "  test             - Executa todos os testes localmente"
	@echo "  test-unit        - Executa apenas os testes unitários"
	@echo "  test-integration - Executa apenas os testes de integração"
	@echo "  test-verbose     - Executa todos os testes com saída detalhada"
	@echo "  test-cov         - Executa testes e exibe relatório de cobertura (local)"
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
	@echo "  compose-test-cov - Executa testes com relatório de cobertura no contêiner"
	@echo "  compose-shell    - Abre um terminal interativo no contêiner backend"
	@echo "  compose-clean    - Para os contêineres e remove volumes (reseta o banco)"

# --- Comandos Locais ---
run:
	@echo "Iniciando aplicação localmente..."
	cd $(APP_DIR) && poetry run uvicorn app.main:app --reload --port $(PORT)

test:
	@echo "Executando testes locais..."
	cd $(APP_DIR) && poetry run pytest

test-unit:
	@echo "Executando testes unitários..."
	cd $(APP_DIR) && poetry run pytest tests/unit

test-integration:
	@echo "Executando testes de integração..."
	cd $(APP_DIR) && poetry run pytest tests/integration

test-verbose:
	@echo "Executando testes locais com saída detalhada..."
	cd $(APP_DIR) && poetry run pytest -v

test-cov:
	@echo "Executando testes com relatório de cobertura..."
	cd $(APP_DIR) && poetry run pytest --cov=app --cov-report=term-missing

clean:
	@echo "Limpando arquivos temporários locais..."
	cd $(APP_DIR) && find . -type d -name "__pycache__" -prune -exec rm -rf {} +
	cd $(APP_DIR) && find . -type f \( -name "*.pyc" -o -name "*.pyo" \) -delete
	cd $(APP_DIR) && rm -rf .pytest_cache .ruff_cache

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

compose-test-cov:
	@echo "Executando testes com cobertura dentro do contêiner backend..."
	docker compose exec backend poetry run pytest --cov=app --cov-report=term-missing

compose-shell:
	@echo "Acessando terminal do contêiner backend..."
	docker compose exec backend /bin/sh

compose-clean:
	@echo "Removendo contêineres, redes e volumes persistentes..."
	docker compose down -v