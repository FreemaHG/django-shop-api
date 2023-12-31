# API для интернет-магазина Megano
Проект представляет собой API для интернет-магазина, написанный на python с использованием Django Rest Framework.
Frontend реализован на Vue3.

## Оглавление
1. [Инструменты](#Инструменты)
2. [Функционал](#Функционал)
3. [Установка](#Установка)
4. [Скриншоты](#Скриншоты)

## Инструменты
* **Python** (3.11);
* **Django Rest Framework** (Web Framework for API);
* **MySQL** (database);
* **Redis** (message broker for celery);
* **Celery** (background tasks);
* **Flower** (tracking background tasks);
* **logging** (logging);
* **Docker** and **Docker Compose** (containerization);
* **Gunicorn** (WSGI HTTP Server);
* **Nginx** (Web Server);
* **Vue3** (Frontend Framework).

## Функционал
*Приложение позволяет*:
- Создавать товары различных категорий (в т.ч. вложенных);
- Оставлять комментарии к товарам;
- Выполнять поиск, фильтровать и сортировать товары по различным параметрам;
- Регистрироваться и создавать профиль с отслеживанием истории покупок;
- Добавлять товары в корзину, удалять и менять кол-во товара в корзине 
(как для авторизованных, так и неавторизованных пользователей);
- Оформлять заказ с вводом и оплаты заказа по фиктивным данным (имитация оплаты заказа в фоне при помощи Celery).

## Установка

1. Копируем содержимое репозитория в отдельный каталог:
```
git clone https://github.com/FreemaHG/django-shop-api.git
```
2. Переименовываем файл "**.env.template**" в "**.env**", при необходимости можно задать свои параметры.

3. Собираем и запускаем контейнеры с приложением. В терминале в общей директории (с файлом "docker-compose.yml") 
вводим команду:
```
docker-compose up -d
```

4. Применяем миграции (создаем БД с зависимостями):
```
docker-compose exec api python3 -m src.manage migrate
```

5. Загрузка демонстрационных данных (опционально):
```
docker-compose exec api python3 -m src.manage loaddata fixtures/db.json
```

Добавятся записи с товарами, комментариями, заказами и суперпользователем:
  - логин: admin; 
  - пароль: admin.

6. Создание суперпользователя (опционально):
```
docker-compose exec api python3 -m src.manage createsuperuser
```
Приложение запускается автоматически и доступно по адресу: `http://<domen>/`

Админка: `http://<domen>/admin/`

Документация API: `http://<domen>/swagger/`

**ВАЖНО**: домен задается в файле **.env** в переменной окружения **DOMEN_HOST**.

## Скриншоты
![](/screen/1.png)
![](/screen/2.png)
![](/screen/3.png)
![](/screen/4.png)
![](/screen/5.png)
![](/screen/6.png)
