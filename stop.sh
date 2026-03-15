set -e

COMPOSE_FILE=docker-compose.yml

echo "🔹 Parando containers e removendo volumes..."
docker compose -f $COMPOSE_FILE down -v
