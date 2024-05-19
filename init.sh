#!/bin/bash

if [ "$(id -u)" -ne 0 ]; then
  echo "Скрипт должен быть запущен с правами root."
  exit 1
fi

USER=${SUDO_USER:-$(whoami)}

sudo -u $USER <<EOF

sudo docker-compose up --build -d

sudodocker-compose exec web python manage.py makemigrations app
sudo docker-compose exec web python manage.py migrate
sudo docker-compose exec web python manage.py shell -c "exec(open('add_superuser.py').read())" 

sudo docker-compose cp db/add_default_data.sql db:/
sudo docker-compose exec db psql -U admin -d huonix -f /add_default_data.sql

sudo echo "Docker Compose is up and running!"

EOF