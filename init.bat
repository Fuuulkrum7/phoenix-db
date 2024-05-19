docker-compose up --build -d
docker-compose exec web python manage.py makemigrations app
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py shell -c "exec(open('add_superuser.py').read())" 
docker-compose cp db/add_default_data.sql db:/
docker-compose exec db psql -U admin -d huonix -f /add_default_data.sql