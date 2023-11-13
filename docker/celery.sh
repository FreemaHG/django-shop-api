#!/bin/bash

# Если передан аргумент "celery"
if [[ "${1}" == "celery" ]]; then
  # Запуску celery с выводом логов уровня INFO
  celery --app=src.megano.celery:app worker -l INFO
# Если передан аргумент "flower"
elif [[ "${1}" == "flower" ]]; then
  # Запускаем flower через celery
  celery --app=src.megano.celery:app flower -l INFO
fi