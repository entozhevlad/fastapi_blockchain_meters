# database_service/Dockerfile

# Используем официальный образ Python
FROM python:3.10-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем requirements.txt и устанавливаем зависимости
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Устанавливаем Alembic
RUN pip install alembic

# Копируем код микросервиса и shared директорию
COPY . .
COPY ./shared ./shared
COPY ./alembic ./alembic
COPY ./alembic.ini ./alembic.ini

# Указываем команду запуска FastAPI приложения
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8002"]
