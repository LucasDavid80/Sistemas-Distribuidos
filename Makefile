PYTHON = python
APP_DIR = backend
PORT = 8001

.PHONY: help frontend backend bd docker run lint format format-check test test-unit test-integration clean db-upgrade db-migration db-current compose-up compose-down compose-logs compose-ps compose-clean compose-shell compose-backend compose-db compose-test frontend-install frontend-dev frontend-lint frontend-format frontend-check frontend-test frontend-test-e2e frontend-build check-all

ifeq ($(filter frontend,$(MAKECMDGOALS)),frontend)
help:
	@echo "Alvos Frontend:"
	@echo "  frontend-install - Instala dependências do frontend com npm ci"
	@echo "  frontend-dev     - Inicia o servidor Vite"
	@echo "  frontend-lint    - Executa o lint com Biome"
	@echo "  frontend-format  - Formata o frontend com Biome"
	@echo "  frontend-check   - Verifica lint e formatação do frontend"
	@echo "  frontend-test    - Executa os testes Vitest"
	@echo "  frontend-test-e2e - Executa os testes E2E com Playwright"
	@echo "  frontend-build   - Gera o build de produção"
	@echo "  check-all        - Valida backend e frontend"

frontend:
	@:

else ifeq ($(filter backend,$(MAKECMDGOALS)),backend)
help:
	@echo "Alvos do Backend:"
	@echo "  run              - Executa a aplicação localmente com Poetry"
	@echo "  lint             - Verifica a qualidade do código com Ruff"
	@echo "  format           - Formata o código com Ruff"
	@echo "  format-check     - Verifica a formatação com Ruff"
	@echo "  test             - Executa todos os testes localmente"
	@echo "  test-unit        - Executa apenas os testes unitários"
	@echo "  test-integration - Executa apenas os testes de integração"
	@echo "  test-verbose     - Executa todos os testes com saída detalhada"
	@echo "  test-cov         - Executa testes e exibe relatório de cobertura (local)"
	@echo "  clean            - Limpa arquivos temporários locais (__pycache__)"

backend:
	@:

else ifeq ($(filter bd,$(MAKECMDGOALS)),bd)
help:
	@echo "Alvos do Banco de Dados:"
	@echo "  db-upgrade       - Aplica as migrations até a revisão head"
	@echo "  db-migration     - Gera uma migration com autogenerate (use msg='...')"
	@echo "  db-current       - Exibe a revisão atual do banco"

bd:
	@:

else ifeq ($(filter docker,$(MAKECMDGOALS)),docker)
help:
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

docker:
	@:

else
help:
	@echo "Uso: make [alvo]"
	@echo ""
	@echo "Alvos Locais:"
	@echo "  help             - Exibe todos os comandos disponíveis"
	@echo "  help frontend    - Exibe apenas os comandos do frontend"
	@echo "  help backend     - Exibe apenas os comandos do backend"
	@echo "  help bd          - Exibe apenas os comandos do banco de dados"
	@echo "  help docker      - Exibe apenas os comandos Docker Compose"
	@echo "  run              - Executa a aplicação localmente com Poetry"
	@echo "  lint             - Verifica a qualidade do código com Ruff"
	@echo "  format           - Formata o código com Ruff"
	@echo "  format-check     - Verifica a formatação com Ruff"
	@echo "  test             - Executa todos os testes localmente"
	@echo "  test-unit        - Executa apenas os testes unitários"
	@echo "  test-integration - Executa apenas os testes de integração"
	@echo "  test-verbose     - Executa todos os testes com saída detalhada"
	@echo "  test-cov         - Executa testes e exibe relatório de cobertura (local)"
	@echo ""
	@echo "Alvos Frontend:"
	@echo "  frontend-install - Instala dependências do frontend com npm ci"
	@echo "  frontend-dev     - Inicia o servidor Vite"
	@echo "  frontend-lint    - Executa o lint com Biome"
	@echo "  frontend-format  - Formata o frontend com Biome"
	@echo "  frontend-check   - Verifica lint e formatação do frontend"
	@echo "  frontend-test    - Executa os testes Vitest"
	@echo "  frontend-test-e2e - Executa os testes E2E com Playwright"
	@echo "  frontend-build   - Gera o build de produção"
	@echo "  check-all        - Valida backend e frontend"
	@echo "  db-upgrade       - Aplica as migrations até a revisão head"
	@echo "  db-migration     - Gera uma migration com autogenerate (use msg='...')"
	@echo "  db-current       - Exibe a revisão atual do banco"
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
endif

# --- Comandos Locais ---
run:
	@echo "Iniciando aplicação localmente..."
	cd $(APP_DIR) && poetry run uvicorn app.main:app --reload --port $(PORT)

lint:
	@echo "Verificando a qualidade do código..."
	cd $(APP_DIR) && poetry run ruff check .

format:
	@echo "Formatando o código..."
	cd $(APP_DIR) && poetry run ruff format .

format-check:
	@echo "Verificando a formatação do código..."
	cd $(APP_DIR) && poetry run ruff format --check .

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

db-upgrade:
	@echo "Aplicando migrations..."
	cd $(APP_DIR) && poetry run alembic upgrade head

db-migration:
	@test -n "$(msg)" || (echo "Uso: make db-migration msg=\"descrição da migration\""; exit 1)
	@echo "Gerando migration: $(msg)"
	cd $(APP_DIR) && poetry run alembic revision --autogenerate -m "$(msg)"

db-current:
	@echo "Consultando revisão atual do banco..."
	cd $(APP_DIR) && poetry run alembic current

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

# --- Frontend ---
frontend-install:
	npm --prefix frontend ci

frontend-dev:
	npm --prefix frontend run dev

frontend-lint:
	npm --prefix frontend run lint

frontend-format:
	npm --prefix frontend run format

frontend-check:
	npm --prefix frontend run lint
	npm --prefix frontend run format:check

frontend-test:
	npm --prefix frontend run test

frontend-test-e2e:
	npm --prefix frontend run test:e2e

frontend-build:
	npm --prefix frontend run build

check-all:
	$(MAKE) lint
	$(MAKE) format-check
	$(MAKE) test
	$(MAKE) frontend-check
	$(MAKE) frontend-test
	$(MAKE) frontend-build
	$(MAKE) frontend-test-e2e
