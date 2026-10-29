# Sistemas-Distribuidos
Repositório para códigos da Matéria de Sistemas Distribuídos

## Frontend — Prática 6

O diretório `frontend/` contém um marketplace local em React: vendedores publicam produtos e compradores visualizam as ofertas. Nesta prática os produtos ficam apenas no estado do navegador; não há chamadas ao backend.

Com o Node.js 22 ou superior instalado, execute a partir da raiz:

```bash
make frontend-install
make frontend-dev
```

Para validar o projeto:

```bash
make frontend-check
make frontend-test
make frontend-build
make frontend-test-e2e
```

## Como executar os testes (Prática 3)

Neste projeto utilizamos a ferramenta `pytest` para a execução dos testes automatizados. O repositório já conta com um Makefile para facilitar o processo.

Para executar todos os testes da aplicação backend, basta rodar o comando abaixo a partir da pasta raiz do projeto (`lab/`):

```bash
make test
```

Alternativamente, você pode rodar acessando a pasta e usando o poetry diretamente:

```bash
cd backend
poetry run pytest
```
