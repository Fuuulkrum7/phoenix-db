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


## Information about development process

https://drawsql.app/teams/fuuulkrum7/diagrams/shalash

## Installation

Clone the repository:

```
git clone https://github.com/Vanillla-Ice/phoenix-db/tree/main
```

Change into the repository directory:

```
cd phoenix-bd
```

* If you are on Linux, you need to use sudo to run next commands:

### Install manually
For Linux:
```
sudo docker-compose exec web python manage.py migrate
sudo docker-compose exec web python manage.py makemigrations app
sudo docker-compose exec web python manage.py createsuperuser
sudo dock
```

### Build the Docker image:
For Linux:
```
sudo  ./init.sh
```
For Windows:
```
init.bat
```
### Restart the Docker Compose:
For Linux:
```
sudo ./restart.sh
```
For Windows:
```
restart.bat
```

### Doxygen
Install doxygen

linux
sudo 
```
apt install doxygen
```
mac
```
brew install doxygen
```
windows
https://www.doxygen.nl/download.html

Now run doxygen:

```
cd <work-dir>
doxygen doxyfile
```

