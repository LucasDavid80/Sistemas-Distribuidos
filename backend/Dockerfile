FROM python:3.13-slim

WORKDIR /app

# Evita que o Python gere arquivos .pyc e faz o stdout/stderr saírem sem buffer
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    POETRY_VIRTUALENVS_CREATE=false

# Instala o Poetry
RUN pip install --no-cache-dir poetry

# Copia os arquivos de definição de dependências
COPY pyproject.toml poetry.lock* ./

# Instala as dependências
RUN poetry install --no-interaction --no-ansi --no-root

# Copia o código da aplicação
COPY . .

# Expõe a porta da aplicação
EXPOSE 8000

# Comando padrão de inicialização
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
