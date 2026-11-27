PYTHON = python
APP_DIR = backend
PORT = 8001

.PHONY: help frontend backend bd docker run lint format format-check test test-unit test-integration clean db-upgrade db-migration db-current create-demo-seller up-build down compose-up compose-down compose-logs compose-ps compose-clean compose-shell compose-api compose-db compose-test frontend-install frontend-dev frontend-lint frontend-format frontend-check frontend-test frontend-test-cov frontend-test-e2e frontend-build frontend-clean e2e check-all

ifeq ($(filter frontend,$(MAKECMDGOALS)),frontend)
help:
	@echo "Alvos Frontend:"
	@echo "  frontend-install  - Instala dependencias do frontend com npm ci"
	@echo "  frontend-dev      - Inicia o servidor Vite"
	@echo "  frontend-lint     - Executa o lint com Biome"
	@echo "  frontend-format   - Formata o frontend com Biome"
	@echo "  frontend-check    - Verifica lint e formatacao do frontend"
	@echo "  frontend-test     - Executa os testes Vitest"
	@echo "  frontend-test-cov - Executa os testes Vitest com relatorio de cobertura"
	@echo "  frontend-test-e2e - Executa os testes E2E com Playwright (requer infra rodando)"
	@echo "  frontend-build    - Gera o build de producao"
	@echo "  frontend-clean    - Remove dist, coverage, playwright-report e test-results"

frontend:
	@:

else ifeq ($(filter backend,$(MAKECMDGOALS)),backend)
help:
	@echo "Alvos do Backend:"
	@echo "  run              - Executa a aplicacao localmente com Poetry"
	@echo "  lint             - Verifica a qualidade do codigo com Ruff"
	@echo "  format           - Formata o codigo com Ruff"
	@echo "  format-check     - Verifica a formatacao com Ruff"
	@echo "  test             - Executa todos os testes localmente"
	@echo "  test-unit        - Executa apenas os testes unitarios"
	@echo "  test-integration - Executa apenas os testes de integracao"
	@echo "  test-verbose     - Executa todos os testes com saida detalhada"
	@echo "  test-cov         - Executa testes e exibe relatorio de cobertura (local)"
	@echo "  clean            - Limpa arquivos temporarios locais (__pycache__)"

backend:
	@:

else ifeq ($(filter bd,$(MAKECMDGOALS)),bd)
help:
	@echo "Alvos do Banco de Dados:"
	@echo "  db-upgrade    - Aplica as migrations ate a revisao head"
	@echo "  db-migration  - Gera uma migration com autogenerate (use msg='...')"
	@echo "  db-current    - Exibe a revisao atual do banco"

bd:
	@:

else ifeq ($(filter docker,$(MAKECMDGOALS)),docker)
help:
	@echo "Alvos Docker Compose:"
	@echo "  compose-up       - Constroi e sobe todos os servicos em segundo plano"
	@echo "  compose-down     - Para e remove todos os conteineres e redes"
	@echo "  compose-api      - Sobe apenas o servico da API (e dependencias)"
	@echo "  compose-db       - Sobe apenas o banco de dados PostgreSQL"
	@echo "  compose-logs     - Acompanha os logs dos conteineres em tempo real"
	@echo "  compose-ps       - Exibe o status e as portas dos conteineres"
	@echo "  compose-test     - Executa os testes unitarios dentro do conteiner backend"
	@echo "  compose-test-cov - Executa testes com relatorio de cobertura no conteiner"
	@echo "  compose-shell    - Abre um terminal interativo no conteiner backend"
	@echo "  compose-clean    - Para os conteineres e remove volumes (reseta o banco)"

docker:
	@:

else
help:
	@echo "Uso: make [alvo]"
	@echo ""
	@echo "Helpers:"
	@echo "  help             - Exibe todos os comandos disponiveis"
	@echo "  help backend     - Exibe apenas os comandos do backend"
	@echo "  help bd          - Exibe apenas os comandos do banco de dados"
	@echo "  help docker      - Exibe apenas os comandos Docker Compose"
	@echo "  help frontend    - Exibe apenas os comandos do frontend"
	@echo ""
	@echo "Backend (Local):"
	@echo "  run              - Executa a aplicacao localmente com Poetry"
	@echo "  lint             - Verifica a qualidade do codigo com Ruff"
	@echo "  format           - Formata o codigo com Ruff"
	@echo "  format-check     - Verifica a formatacao com Ruff"
	@echo "  test             - Executa todos os testes localmente"
	@echo "  test-unit        - Executa apenas os testes unitarios"
	@echo "  test-integration - Executa apenas os testes de integracao"
	@echo "  test-verbose     - Executa todos os testes com saida detalhada"
	@echo "  test-cov         - Executa testes e exibe relatorio de cobertura (local)"
	@echo "  clean            - Limpa arquivos temporarios locais (__pycache__)"
	@echo ""
	@echo "Banco de Dados:"
	@echo "  db-upgrade    - Aplica as migrations ate a revisao head"
	@echo "  db-migration  - Gera uma migration com autogenerate (use msg='...')"
	@echo "  db-current    - Exibe a revisao atual do banco"
	@echo ""
	@echo "Docker Compose:"
	@echo "  compose-up       - Constroi e sobe todos os servicos em segundo plano"
	@echo "  compose-down     - Para e remove todos os conteineres e redes"
	@echo "  compose-api      - Sobe apenas o servico da API (e dependencias)"
	@echo "  compose-db       - Sobe apenas o banco de dados PostgreSQL"
	@echo "  compose-logs     - Acompanha os logs dos conteineres em tempo real"
	@echo "  compose-ps       - Exibe o status e as portas dos conteineres"
	@echo "  compose-test     - Executa os testes unitarios dentro do conteiner backend"
	@echo "  compose-test-cov - Executa testes com relatorio de cobertura no conteiner"
	@echo "  compose-shell    - Abre um terminal interativo no conteiner backend"
	@echo "  compose-clean    - Para os conteineres e remove volumes (reseta o banco)"
	@echo ""
	@echo "Frontend:"
	@echo "  frontend-install  - Instala dependencias do frontend com npm ci"
	@echo "  frontend-dev      - Inicia o servidor Vite"
	@echo "  frontend-lint     - Executa o lint com Biome"
	@echo "  frontend-format   - Formata o frontend com Biome"
	@echo "  frontend-check    - Verifica lint e formatacao do frontend"
	@echo "  frontend-test     - Executa os testes Vitest"
	@echo "  frontend-test-cov - Executa os testes Vitest com relatorio de cobertura"
	@echo "  frontend-test-e2e - Executa os testes E2E com Playwright (requer infra rodando)"
	@echo "  frontend-build    - Gera o build de producao"
	@echo "  frontend-clean    - Remove dist, coverage, playwright-report e test-results"
	@echo ""
	@echo "CI / Validacao Global:"
	@echo "  check-all - Valida backend e frontend (lint+test+build+e2e)"
	@echo "  e2e       - Sobe ambiente completo e executa testes E2E"
endif

# --- Comandos Locais ---
run:
	@echo "Iniciando aplicacao localmente..."
	cd $(APP_DIR) && poetry run uvicorn app.main:app --reload --port $(PORT)

lint:
	@echo "Verificando a qualidade do codigo..."
	cd $(APP_DIR) && poetry run ruff check .

format:
	@echo "Formatando o codigo..."
	cd $(APP_DIR) && poetry run ruff format .

format-check:
	@echo "Verificando a formatacao do codigo..."
	cd $(APP_DIR) && poetry run ruff format --check .

test:
	@echo "Executando testes locais..."
	cd $(APP_DIR) && poetry run pytest

test-unit:
	@echo "Executando testes unitarios..."
	cd $(APP_DIR) && poetry run pytest tests/unit

test-integration:
	@echo "Executando testes de integracao..."
	cd $(APP_DIR) && poetry run pytest tests/integration

test-verbose:
	@echo "Executando testes locais com saida detalhada..."
	cd $(APP_DIR) && poetry run pytest -v

test-cov:
	@echo "Executando testes com relatorio de cobertura..."
	cd $(APP_DIR) && poetry run pytest --cov=app --cov-report=term-missing

db-upgrade:
	@echo "Aplicando migrations..."
	cd $(APP_DIR) && poetry run alembic upgrade head

db-migration:
	@test -n "$(msg)" || (echo "Uso: make db-migration msg=\"descricao da migration\""; exit 1)
	@echo "Gerando migration: $(msg)"
	cd $(APP_DIR) && poetry run alembic revision --autogenerate -m "$(msg)"

db-current:
	@echo "Consultando revisao atual do banco..."
	cd $(APP_DIR) && poetry run alembic current

create-demo-seller:
	@echo "Criando ou verificando o vendedor demo..."
	docker compose exec api poetry run python -m scripts.create_demo_seller

clean:
	@echo "Limpando arquivos temporarios locais..."
	cd $(APP_DIR) && find . -type d -name "__pycache__" -prune -exec rm -rf {} +
	cd $(APP_DIR) && find . -type f \( -name "*.pyc" -o -name "*.pyo" \) -delete
	cd $(APP_DIR) && rm -rf .pytest_cache .ruff_cache

# --- Comandos Docker Compose ---
compose-up:
	@echo "Subindo todos os servicos com Docker Compose..."
	docker compose up -d --build

up-build: compose-up

down: compose-down

compose-down:
	@echo "Parando todos os servicos..."
	docker compose down

compose-api:
	@echo "Subindo o servico da API..."
	docker compose up -d --build api

compose-db:
	@echo "Subindo apenas o banco de dados PostgreSQL..."
	docker compose up -d db

compose-logs:
	@echo "Exibindo logs dos conteineres..."
	docker compose logs -f

compose-ps:
	@echo "Status dos servicos:"
	docker compose ps

compose-test:
	@echo "Executando testes dentro do conteiner backend..."
	docker compose exec backend poetry run pytest

compose-test-cov:
	@echo "Executando testes com cobertura dentro do conteiner backend..."
	docker compose exec backend poetry run pytest --cov=app --cov-report=term-missing

compose-shell:
	@echo "Acessando terminal do conteiner backend..."
	docker compose exec backend /bin/sh

compose-clean:
	@echo "Removendo conteineres, redes e volumes persistentes..."
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

frontend-test-cov:
	@echo "Executando testes com relatorio de cobertura do frontend..."
	npm --prefix frontend run test:cov

frontend-test-e2e:
	npm --prefix frontend run test:e2e

frontend-build:
	npm --prefix frontend run build

frontend-clean:
	@echo "Limpando arquivos temporarios do frontend..."
	if exist frontend\dist rmdir /s /q frontend\dist
	if exist frontend\coverage rmdir /s /q frontend\coverage
	if exist frontend\playwright-report rmdir /s /q frontend\playwright-report
	if exist frontend\test-results rmdir /s /q frontend\test-results

e2e:
	docker compose -p c216-e2e -f docker-compose.yml -f docker-compose.e2e.yml up -d --build
	docker compose -p c216-e2e -f docker-compose.yml -f docker-compose.e2e.yml exec -T api poetry run alembic upgrade head
	docker compose -p c216-e2e -f docker-compose.yml -f docker-compose.e2e.yml exec -T api poetry run python -m scripts.create_demo_seller
ifeq ($(OS),Windows_NT)
	set E2E_BASE_URL=http://127.0.0.1:5174&& set VITE_API_URL=http://127.0.0.1:8002&& set VITE_USER_ID=1&& npm --prefix frontend run test:e2e
else
	E2E_BASE_URL=http://127.0.0.1:5174 VITE_API_URL=http://127.0.0.1:8002 VITE_USER_ID=1 npm --prefix frontend run test:e2e
endif
	docker compose -p c216-e2e -f docker-compose.yml -f docker-compose.e2e.yml down -v

check-all:
	$(MAKE) lint
	$(MAKE) format-check
	$(MAKE) test
	$(MAKE) frontend-check
	$(MAKE) frontend-test
	$(MAKE) frontend-build
	$(MAKE) e2e
