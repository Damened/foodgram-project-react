# Продуктовый помощник Foodgram - дипломный проект. Яндекс.Практикум

## Описание проекта Foodgram
### Проект «Фудграм»  приложение, на котором пользователи публикуют рецепты кулинарных изделий, подписываться на публикации других авторов и добавлять рецепты в свое избранное, так же позволяет скачивать список покупок. Сайт доступен http://damenedfinal.ddns.net

#Стек технологий.
- Python 3.9
- Django 3.2
- djangorestframework 3.14
- Gunicorn
- Nginx
- PostgreSQL
- Docker

# Установить Docker и docker-compose
## Клонировать репозиторий и перейти в него в командной строке:
### git clone git@github.com:Damened/foodgram-project-react.git
- cd foodgram-project-react/

## В корневой папке проекта создайте файл .env, в котором заполните следующие переменные окружения:
- POSTGRES_DB=foodgram
- POSTGRES_USER=foodgram_user
- POSTGRES_PASSWORD=foodgram_password
- DB_HOST=db6
- DB_PORT=5432

## Запустите docker-compose в корневой директории командой:
- docker compose up -d --build

## Выполните миграции, соберите статику и копируйте её в необходимую дерикторию:
- :docker compose exec backend python manage.py makemigrations users

- :docker compose exec backend python manage.py makemigrations recipes

- :docker compose exec backend python manage.py migrate

- :docker compose exec backend python manage.py collectstatic

- :docker compose exec backend cp -r /app/collected_static/. /backend_static/static/

## Создайте суперюзера и загрузите предустановленый список ингредиентов
- :docker compose exec backend python manage.py createsuperuser

- :docker compose exec backend python manage.py load_data
## Проверить работу
- http://127.0.0.1:8800/
## Документация
- http://127.0.0.1:8800/api/docs/

## сайт доступен по адресу 
### http://damenedfinal.ddns.net

## для проверки 
### admin: http://damenedfinal.ddns.net/admin
- email: admin@mail.ru
- password: 123321

## test user простой пользователь для проверки подписки и скачивание 
- email: test1@mail.ru
- password: 12345678Qw
- email: test2@mail.ru
- password: 12345678Qw