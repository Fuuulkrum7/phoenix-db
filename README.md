# phoenix-bd
Should add later

git clone https://github.com/

docker-compose up --build -d

docker-compose exec db psql -U admin

create database huonix;

\q

docker-compose exec web python manage.py migrate

docker-compose exec web python manage.py createsuperuser
