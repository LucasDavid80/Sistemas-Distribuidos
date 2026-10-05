# Sistemas-Distribuidos
Repositório para códigos da Matéria de Sistemas Distribuídos

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
