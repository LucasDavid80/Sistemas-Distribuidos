# Sistemas Distribuídos — Prática 7

Este diretório contém o marketplace da Prática 7, composto por um frontend React, uma API FastAPI e um banco PostgreSQL. A forma recomendada de executar e verificar a aplicação é usando os comandos do `Makefile`.

## Pré-requisitos

- Docker Desktop em execução;
- GNU Make;
- Node.js 22 ou superior (necessário para os testes do frontend e E2E);
- Poetry instalado, caso os comandos locais do backend sejam utilizados.

Execute todos os comandos a partir deste diretório (`lab/`).

## 1. Preparar o ambiente

No Git Bash, crie o arquivo de configuração:

```bash
cp .env.example .env
```

No PowerShell, use:

```powershell
Copy-Item .env.example .env
```

O comando `copy` não é válido no Git Bash.

## 2. Subir a aplicação

Construa as imagens e inicie o PostgreSQL, a API e o frontend:

```bash
make up-build
make compose-ps
```

Os serviços devem aparecer como em execução/saudáveis. A aplicação fica disponível em:

- Frontend: <http://localhost:5173>
- API: <http://localhost:8001>
- Health check: <http://localhost:8001/health>
- PostgreSQL: `localhost:5433` (dentro da rede Docker, a API usa `db:5432`)

## 3. Preparar o banco de dados

O target `db-upgrade` executa o Alembic localmente. Por isso, informe a URL do PostgreSQL publicado pelo Docker antes de executá-lo.

No Git Bash:

```bash
export DATABASE_URL=postgresql://postgres:postgres@localhost:5433/app_db
make db-upgrade
```

No PowerShell:

```powershell
$env:DATABASE_URL = "postgresql://postgres:postgres@localhost:5433/app_db"
make db-upgrade
```

Depois, crie o vendedor usado pelo frontend:

```bash
make create-demo-seller
```

O frontend usa `VITE_USER_ID=1` por padrão. Se o comando acima informar outro ID, atualize `VITE_USER_ID` no arquivo `.env` e execute `make up-build` novamente.

## 4. Verificação manual da Prática 7

Com os serviços ativos e o banco preparado:

1. Acesse <http://localhost:5173>.
2. Selecione o perfil de vendedor.
3. Publique um produto preenchendo os dados obrigatórios.
4. Confirme que o produto aparece na listagem e que não há mensagem de erro.
5. Selecione o perfil de comprador.
6. Confirme que o produto publicado pelo vendedor está visível para o comprador.
7. Tente publicar um produto sem preencher os campos obrigatórios.
8. Confirme que a validação é exibida e que nenhum produto inválido é criado.

Para acompanhar problemas durante a verificação:

```bash
make compose-logs
```

## 5. Validações automatizadas

Execute os checks do frontend:

```bash
make frontend-check
make frontend-test
make frontend-build
```

Esses comandos verificam, respectivamente, lint/formatação, testes Vitest e o build de produção.

O teste E2E do frontend, usando a aplicação que já está rodando em `localhost:5173`, é executado com:

```bash
make frontend-test-e2e
```

## 6. E2E full-stack isolado

Para executar o cenário completo com containers próprios de API, frontend e PostgreSQL, use a stack E2E isolada:

```bash
make down
make e2e
```

O target `e2e` sobe os serviços isolados, aplica as migrations, cria o vendedor demo, executa o Playwright e remove a stack E2E ao terminar. Ela usa API em `8002`, frontend em `5174` e PostgreSQL em `5434`, sem conflitar com a stack principal.

Se o comando for interrompido antes da limpeza, remova a stack E2E antes de tentar novamente:

```bash
docker compose -p c216-e2e -f docker-compose.yml -f docker-compose.e2e.yml down -v
```

## 7. Comando de verificação completa

Para executar todas as verificações previstas pelo projeto:

```bash
make down
make check-all
```

O comando executa as validações do backend, frontend, testes, build e E2E.

## Comandos úteis

```bash
make help          # lista os targets disponíveis
make compose-ps    # mostra o estado dos containers
make compose-logs  # acompanha os logs
make down          # para a aplicação
make compose-clean # para a aplicação e apaga o volume do banco
```

Use `make compose-clean` somente quando quiser recriar o banco do zero, pois ele remove os dados persistidos pelo PostgreSQL.
