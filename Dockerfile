FROM python:3.12-slim

# Установка системных зависимостей
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Создаем пользователя с UID 1000 (требование Hugging Face)
RUN useradd -m -u 1000 user
USER user
ENV HOME=/home/user \
    PATH=/home/user/.local/bin:$PATH

WORKDIR $HOME/app

# Копируем файлы проекта и ставим зависимости
COPY --chown=user:user requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY --chown=user:user . .

# Собираем статические файлы и применяем миграции (опционально для SQLite)
RUN python manage.py collectstatic --noinput

# Запускаем Django через Gunicorn на порту 7860
CMD ["gunicorn", "algorithm_website_project.wsgi:application", "--bind", "0.0.0.0:7860"]