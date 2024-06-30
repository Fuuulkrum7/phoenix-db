#!/bin/bash

if [ "$(id -u)" -ne 0 ]; then
  echo "Скрипт должен быть запущен с правами root."
  exit 1
fi

## USER=${SUDO_USER:-$(whoami)}

## sudo -u $USER <<EOF

docker-compose up --build -d

docker-compose exec web python manage.py makemigrations app
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py shell -c "exec(open('add_superuser.py').read())" 

docker compose cp db/add_default_data.sql db:/
docker compose cp db/init_triggers.sql db:/

docker-compose exec db psql -U admin -d huonix -f init_triggers.sql
docker-compose exec db psql -U admin -d huonix -f add_default_data.sql

echo "Docker Compose is up and running!"
