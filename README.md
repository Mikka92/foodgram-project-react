<a id='start_page'></a>
# <p align = center>Продуктовый помошник "Foodgram"</p>
___
[![foodgram-app workflow](https://github.com/Mikka92/foodgram-project-react/actions/workflows/main.yml/badge.svg)](https://github.com/Mikka92/foodgram-project-react/actions/workflows/main.yml)

### Описание проекта

«Foodgram» - это сайт, на котором пользователи будут публиковать рецепты, добавлять чужие рецепты в избранное и подписываться на публикации других авторов. Сервис «Список покупок» позволит пользователям создавать список продуктов, которые нужно купить для приготовления выбранных блюд.


  [![](https://img.shields.io/badge/Python-3.7.9-blue)](https://www.python.org/downloads/release/python-379/) [![](https://img.shields.io/badge/Django-3.2.16-green)](https://docs.djangoproject.com/en/4.1/releases/3.2.16/) [![](https://img.shields.io/badge/DRF-3.2.14-orange)](https://www.django-rest-framework.org/community/release-notes/#3124) [![](https://img.shields.io/badge/Docker-23.0.6-blue)](https://docs.docker.com/engine/release-notes/23.0/) [![](https://img.shields.io/badge/Nginx-1.21.3-green)](https://docs.docker.com/engine/release-notes/23.0/) [![](https://img.shields.io/badge/PostgreSQL-13.0-orange)](https://docs.docker.com/engine/release-notes/23.0/)

### Проект доступен по IP-адресу:
```
158.160.31.126/recipes
```
### Войти администратором:
```
158.160.31.126/admin
Почта: mikkazed@yandex.ru
Пароль: Mikka92!
```
### Как запустить проект:
1. Клонировать репозиторий и перейти в infra:
```
https://github.com/Mikka92/foodgram-project-react.git
```
```
cd infra/
```
2. Запустить сборку docker-compose:
```
docker-compose up
```
3. Выполнить миграции:
```
docker-compose exec web python manage.py migrate
```
4. Создать суперпользователя:
```
docker-compose exec web python manage.py createsuperuser
```
5. Собираем статику:
```
docker-compose exec web python manage.py collectstatic --no-input
```
Шаблон наполнения env-файла:
```
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432
SECRET_KEY='d4-5%szu2y5mm8470kq!ejy0fz*-hipk4e!ry!u7&7a@z1u^za'
```
### Команды для заполнения базы данными
Копируем файл с базами данных из /infra в папку app:
```
docker cp fixtures.json <CONTAINER ID>:/app
```
Запускаем команду для загрузки баз:
```
docker-compose exec web python manage.py loaddata fixtures.json
```

#### Авторы

><font size=2>Backend - Зименко М.В.  |  Frontend - Yandex Practicum</font>

[наверх](#start_page)
