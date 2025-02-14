# Используем официальный образ Python
FROM python:3.9-slim

# Устанавливаем рабочую директорию
WORKDIR /LiveCoding

# Копируем зависимости
COPY core/requirements.txt .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем исходный код
COPY . .

# Открываем порт 5000
EXPOSE 5000

# Запускаем приложение
CMD ["python", "core/app.py"]