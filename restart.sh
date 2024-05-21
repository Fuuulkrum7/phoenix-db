#!/bin/bash

if [ "$(id -u)" -ne 0 ]; then
  echo "Скрипт должен быть запущен с правами root."
  exit 1
fi

sudo docker-compose down
sudo docker-compose up --build -d
