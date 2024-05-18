# phoenix-bd
Should add later

## Requirements
- Docker
- Docker Compose
- PostgreSQL

On Linux, you can install Docker and Docker Compose with the following commands:

```
sudo apt install docker docker-compose
```
or
```
sudo dnf install docker docker-compose
```
or
```
sudo pacman -S docker docker-compose
```

On macOS, you can install Docker and Docker Compose with the following commands:

```
brew install docker docker-compose
```

On Windows, you can install Docker and Docker Compose from the official website:

https://docs.docker.com/desktop/windows/install/


## Installation

Clone the repository:

```
git clone https://github.com/Vanillla-Ice/phoenix-db/tree/main
```

Change into the repository directory:

```
cd phoenix-bd
```

## If you are on Linux, you need to use sudo to run next commands:

Build the Docker image:

```
docker-compose up --build -d
```

* If you get an error about the database not existing, run:

```
docker-compose exec db psql -U admin -d huonix

create database huonix;

\q
```
Then docker-compose succesfully builded the image(you can check it with docker-compose ps).
```
docker-compose exec web python manage.py createsuperuser

docker-compose exec web python manage.py makemigrations app

docker-compose exec web python manage.py migrate
```

## Doxygen
Install doxygen

linux
sudo apt install doxygen

mac
brew install doxygen

windows
https://www.doxygen.nl/download.html

