# Базовый образ: лёгкий Python 3.12
FROM python:3.12-slim

# Рабочая директория внутри контейнера
WORKDIR /app

# Сначала копируем зависимости — слой кэшируется, пока requirements.txt не меняется
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем код приложения
COPY main.py .

# Порт, на котором слушает uvicorn
EXPOSE 8002

# Запуск FastAPI через uvicorn (доступен снаружи по 0.0.0.0)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8002"]
