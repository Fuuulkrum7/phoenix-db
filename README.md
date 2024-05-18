# phoenix-bd
Should add later

## Requirements
- Docker
- Docker Compose
- PostgreSQL

sudo apt install docker docker-compose

## Installation
git clone https://github.com/

docker-compose up --build -d

If you get an error about the database not existing, run
'''
docker-compose exec db psql -U admin -d huonix

create database huonix;

\q
'''

docker-compose exec web python manage.py migrate

docker-compose exec web python manage.py createsuperuser

'''
RUN python manage.py collectstatic --noinput
'''

## Doxygen
Install doxygen

linux
sudo apt install doxygen

mac
brew install doxygen

windows
https://www.doxygen.nl/download.html

