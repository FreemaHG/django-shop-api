#!/bin/bash

# Сбор статических файлов (для админки Django) для последующей обработки сервером nginx
python3 -m src.manage collectstatic --noinput

# Запуск сервера
gunicorn src.megano.wsgi:application --workers 4 --bind=0.0.0.0:8000
