# Використовуємо офіційний легкий образ Python
FROM python:3.13-slim

# Встановлюємо робочу директорію всередині контейнера
WORKDIR /app

# Запобігаємо створенню .pyc файлів та буферизації виводу (для логів)
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Встановлюємо системні залежності (потрібні для деяких python-пакетів)
RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc libpq-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Копіюємо файл залежностей та встановлюємо їх
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Копіюємо весь код проєкту в контейнер
COPY . .

# Відкриваємо порт 8000
EXPOSE 8000

# Команда запуску (буде перевизначена в docker-compose, але це хороший дефолт)
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]