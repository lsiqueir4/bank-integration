#!/bin/bash
set -e

LOGFILE="/docker-entrypoint-initdb.d/sql_errors.log"

for file in /docker-entrypoint-initdb.d/*.sql; do
    echo "Executando $file..."
    if ! psql -v ON_ERROR_STOP=1 -U "$POSTGRES_USER" -d "$POSTGRES_DB" -f "$file"; then
        echo "ERRO ao executar $file" >> $LOGFILE
    else
        echo "$file executado com sucesso"
    fi
done
