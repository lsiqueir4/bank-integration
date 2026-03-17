set -e

COMPOSE_FILE=docker-compose.yml

echo "🔹 Parando containers e removendo volumes..."
docker compose -f $COMPOSE_FILE down -v

COMPOSE_FILE=docker-compose.test.yml

echo "🔹 Parando containers e removendo volumes..."
docker compose -f $COMPOSE_FILE down -v
