# Используем официальный образ Python
FROM python:3.10-slim

# Устанавливаем зависимости для системы
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    --no-install-recommends && \
    rm -rf /var/lib/apt/lists/*

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файл требований и устанавливаем зависимости Python
COPY requirements.txt /app/
COPY .env /app/
RUN pip install --no-cache-dir -r requirements.txt

# Копируем остальные файлы проекта
COPY . /app/

# Применяем миграции базы данных и собираем статические файлы
RUN python manage.py migrate
RUN python manage.py collectstatic --noinput

# Указываем порт, который будет использован контейнером
EXPOSE 8000

# Команда запуска приложения
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "phoenixdb.wsgi:application"]

