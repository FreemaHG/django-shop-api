FROM python:3.11

COPY requirements/base.txt /src/requirements/base.txt
COPY requirements/prod.txt /src/requirements/prod.txt

RUN pip install --no-cache-dir --upgrade -r /src/requirements/prod.txt

COPY ./src /src
COPY ./frontend /frontend
COPY ./docker /docker
COPY ./fixtures /fixtures

# Создаем папку для сбора статических файлов внутри контейнера командой python3 -m src.manage collectstatic --noinput
# В противном случае Docker не создаст папку и файлы не будут скопированы
RUN mkdir /src/staticfiles

# Данной командой мы разрешаем Docker выполнять все команды в папке docker с расширением .sh (bash-команды),
# которые в нашем случае используются для запуска Celery и Flower (в docker-compose.yml)
RUN chmod a+x docker/*.sh