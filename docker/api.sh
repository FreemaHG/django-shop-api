#!/bin/bash

# Создать миграции
python3 -m src.manage makemigrations

# Применить миграции
python3 -m src.manage migrate

# Создать суперпользователя
python3 -m src.manage createsuperuser

# Запуск сервера
python3 -m src.manage runserver
