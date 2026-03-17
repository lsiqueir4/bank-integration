#!/bin/bash
set -e

ENVIRONMENT=${1:-dev}

if [ "$ENVIRONMENT" = "test" ]; then
  COMPOSE_FILE=docker-compose.test.yml
else
  COMPOSE_FILE=docker-compose.yml
fi

echo "🔹 Ambiente selecionado: $ENVIRONMENT"
echo "🔹 Usando compose: $COMPOSE_FILE"

echo "🔹 Parando containers e removendo volumes..."
docker compose -f $COMPOSE_FILE down -v

echo "🔹 Subindo containers novamente com build..."
docker compose -f $COMPOSE_FILE up --build -d