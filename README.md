# C216 — Sistemas Distribuídos | Projeto Final
## TaskFlow — Sistema de Gestão Distribuída de Tarefas e Projetos

Aplicação web full-stack desenvolvida para o Projeto Final da disciplina **C216 (Sistemas Distribuídos)** no Inatel. O sistema implementa um fluxo funcional completo entre interface web, API RESTful conteinerizada e persistência real com banco de dados PostgreSQL.

---

## 📹 Vídeo Demonstrativo do Projeto

- **Link da apresentação:** [Insira o link do YouTube aqui — Vídeo não listado](https://youtu.be/)
> **Observação:** O vídeo de 5 a 10 minutos apresenta a arquitetura, inicialização com Docker Compose, operações de CRUD em tempo real, verificação de persistência no banco e execução dos testes automatizados.

---

## 🎯 Objetivo e Tema

O **TaskFlow** resolve o problema de acompanhamento e priorização de atividades técnicas e projetos. A aplicação evolui significativamente os conceitos das práticas do semestre ao oferecer:

- **CRUD Completo:** Criação, listagem com múltiplos filtros, edição detalhada e exclusão de tarefas;
- **Transição Rápida de Estados:** Ações contextuais de avanço de fluxo (*Iniciar* tarefa pendente, *Concluir* tarefa em andamento);
- **Painel de Métricas e Produtividade:** Dashboard dinâmico com contadores em tempo real (Total de Tarefas, Pendentes, Em Progresso, Concluídas) e cálculo de taxa de conclusão (%);
- **Filtros e Busca:** Filtragem por status (`PENDENTE`, `EM_PROGRESSO`, `CONCLUIDA`), por prioridade (`ALTA`, `MEDIA`, `BAIXA`) e busca textual por título, descrição ou categoria.

---

## 🛠️ Tecnologias Utilizadas

- **Backend:** Python 3.13, [FastAPI](https://fastapi.tiangolo.com/), [SQLAlchemy 2.0](https://www.sqlalchemy.org/), [Alembic](https://alembic.sqlalchemy.org/), [Pydantic v2](https://docs.pydantic.dev/), [Ruff](https://beta.ruff.rs/docs/), [Pytest](https://docs.pytest.org/);
- **Banco de Dados:** [PostgreSQL 16](https://www.postgresql.org/);
- **Frontend:** [React 19](https://react.dev/), [Vite](https://vitejs.dev/), [Tailwind CSS](https://tailwindcss.com/), [Biome](https://biomejs.dev/), [Vitest](https://vitest.dev/), [Testing Library](https://testing-library.com/);
- **Infraestrutura e CI:** [Docker](https://www.docker.com/), [Docker Compose](https://docs.docker.com/compose/), [GNU Make](https://www.gnu.org/software/make/), [Playwright](https://playwright.dev/), [GitHub Actions](https://github.com/features/actions).

---

## 📂 Estrutura do Repositório

```text
lab/
├── .github/workflows/       # Workflows de CI do GitHub Actions (backend e frontend)
├── backend/
│   ├── alembic/             # Migrações versionadas do banco de dados
│   ├── app/
│   │   ├── api/routes/      # Endpoints REST (tasks, projects, users, commerce)
│   │   ├── core/            # Configurações de ambiente e permissões
│   │   ├── database/        # Configuração do engine e sessão SQLAlchemy
│   │   ├── models/          # Modelos ORM (Task, Project, User, Product, Purchase)
│   │   ├── repositories/    # Camada de acesso a dados (queries e agregações)
│   │   ├── schemas/         # Validação e serialização de dados (Pydantic)
│   │   └── services/        # Regras de negócio e casos de uso
│   ├── tests/               # Testes automatizados unitários e de integração (Pytest)
│   ├── Dockerfile           # Imagem conteinerizada da API
│   └── pyproject.toml       # Dependências gerenciadas via Poetry
├── frontend/
│   ├── src/
│   │   ├── components/      # Componentes React (TaskForm, TaskList, TaskMetrics)
│   │   ├── services/        # Integração HTTP com a API FastAPI
│   │   └── validation.js    # Regras de validação do cliente
│   ├── tests/               # Testes unitários (Vitest), integração e E2E (Playwright)
│   └── Dockerfile           # Imagem conteinerizada do frontend com Nginx/Vite
├── docker-compose.yml       # Orquestração dos serviços (api, frontend, db)
├── docker-compose.e2e.yml   # Stack isolada para testes E2E do CI
└── Makefile                 # Comandos unificados de execução, testes e migrations
```

---

## ⚙️ Pré-requisitos

- **Docker Desktop** instalado e em execução;
- **GNU Make**;
- **Node.js 22+** (para execução local de testes do frontend/Playwright);
- **Poetry** (opcional, para execução do backend fora do container).

---

## 🚀 Como Executar a Aplicação

Todos os comandos devem ser executados a partir da pasta raiz do projeto (`lab/`).

### 1. Configurar Variáveis de Ambiente

No Linux / macOS / Git Bash:
```bash
cp .env.example .env
```

No Windows (PowerShell):
```powershell
Copy-Item .env.example .env
```

### 2. Subir os Contêineres

Construa e inicialize os serviços de banco PostgreSQL, backend FastAPI e frontend React:
```bash
make up-build
make compose-ps
```

### 3. Executar as Migrações do Banco de Dados

Aplique as migrações versionadas do Alembic para criar as tabelas no PostgreSQL:

No Linux / macOS / Git Bash:
```bash
export DATABASE_URL=postgresql://postgres:postgres@localhost:5433/app_db
make db-upgrade
make create-demo-seller
```

No Windows (PowerShell):
```powershell
$env:DATABASE_URL = "postgresql://postgres:postgres@localhost:5433/app_db"
make db-upgrade
make create-demo-seller
```

### 4. Acessar a Aplicação

- **Frontend:** [http://localhost:5173](http://localhost:5173)
- **API FastAPI (Swagger Docs):** [http://localhost:8001/docs](http://localhost:8001/docs)
- **Health check da API:** [http://localhost:8001/health](http://localhost:8001/health)
- **PostgreSQL:** `localhost:5433` (externo) / `db:5432` (rede interna Docker)

---

## 🧪 Validações Automatizadas e Testes

Para garantir conformidade de qualidade e validar a pipeline de CI localmente:

### Validações do Backend (Ruff e Pytest)
```bash
make lint          # Verifica qualidade e tipagem com Ruff
make format-check  # Confere a formatação do código
make test          # Executa todos os testes unitários e de integração
```

### Validações do Frontend (Biome e Vitest)
```bash
make frontend-check # Valida lint e formatação com Biome
make frontend-test  # Executa testes unitários e de componentes
make frontend-build # Compila os assets de produção
```

### Teste Ponta a Ponta (Playwright E2E)
```bash
# Executa a stack E2E full-stack isolada (API, Postgres e Frontend dedicados):
make down
make e2e
```

### Validação Completa (Pipeline Local)
```bash
make down
make check-all
```

---

## 📌 Comandos Úteis do Makefile

```bash
make help          # Exibe todos os comandos disponíveis
make compose-ps    # Mostra o status dos contêineres ativos
make compose-logs  # Exibe os logs dos contêineres em tempo real
make down          # Para todos os contêineres do projeto
make compose-clean # Remove contêineres e apaga os volumes do banco de dados
```
