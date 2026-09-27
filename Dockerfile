FROM python:3.13-slim

# Instalar dependências de sistema, incluindo o gettext para o i18n
RUN apt-get update && apt-get install -y \
    gettext \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Instalar as dependências atualizadas a partir do teu requirements.txt
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar o código fonte do projeto
COPY . .