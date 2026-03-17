#!/bin/bash
set -e

LOGFILE="/docker-entrypoint-initdb.d/sql_errors.log"
SQL_DIR="/sql"

for file in "$SQL_DIR"/*.sql; do
    echo "Executando $file..."

    if ! psql -v ON_ERROR_STOP=1 -U "$POSTGRES_USER" -d "$POSTGRES_DB" -f "$file"; then
        echo "ERRO ao executar $file" | tee -a "$LOGFILE"
    else
        echo "$file executado com sucesso"
    fi
done