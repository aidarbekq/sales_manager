#!/bin/sh
set -e

DB_HOST=${DB_HOST:-db}
DB_PORT=${DB_PORT:-5432}

echo "Waiting for database ${DB_HOST}:${DB_PORT}…"
until pg_isready -q -h "$DB_HOST" -p "$DB_PORT"; do
    sleep 1
done
echo "Database is up 🐘"

python manage.py migrate --noinput
python manage.py collectstatic --noinput

exec gunicorn sales_manager.wsgi:application -b 0.0.0.0:8000
