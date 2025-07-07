FROM python:3.12-slim

# Создаём рабочую папку внутри контейнера
WORKDIR /code

# Копируем файл зависимостей
COPY requirements.txt .

# Обновляем pip и устанавливаем зависимости
RUN pip install --upgrade pip && pip install -r requirements.txt

# Копируем весь проект (настрой под свою структуру)
COPY . .

# Открываем порт (если требуется, по умолчанию Django использует 8000)
EXPOSE 8000

# Команда по умолчанию (можно переопределять в docker-compose)
COPY entrypoint.sh .
RUN chmod +x entrypoint.sh
CMD "./entrypoint.sh"