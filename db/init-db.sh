#!/bin/bash
set -e

# Пример инициализации: создание таблиц, заполнение данными и т.д.
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    CREATE TABLE example_table (
        id SERIAL PRIMARY KEY,
        data VARCHAR(255) NOT NULL
    );
    INSERT INTO example_table (data) VALUES ('Example data');
EOSQL
