# foodgram
[![Python 3.7](https://img.shields.io/badge/python-3.7-blue.svg)](https://www.python.org/downloads/release/python-370/)
[![Django-2.2.16](https://img.shields.io/badge/Django-2.2.16-blue.svg)](https://www.djangoproject.com/download/)
[![DjangoRESTframework-3.12.4](https://img.shields.io/badge/Django%20REST%20Framework-3.12.4-blue.svg)](https://www.django-rest-framework.org)
[![Docker 20.10.12](https://img.shields.io/badge/Docker-20.10.12-blue.svg)](https://docs.docker.com/engine/install/ubuntu/)
[![PostgreSQL](https://img.shields.io/badge/-PostgreSQL-464646?style=flat-square&logo=PostgreSQL)](https://www.postgresql.org/)
[![Nginx](https://img.shields.io/badge/-NGINX-464646?style=flat-square&logo=NGINX)](https://nginx.org/ru/)
[![gunicorn](https://img.shields.io/badge/-gunicorn-464646?style=flat-square&logo=gunicorn)](https://gunicorn.org/)
[![Yandex.Cloud](https://img.shields.io/badge/-Yandex.Cloud-464646?style=flat-square&logo=Yandex.Cloud)](https://cloud.yandex.ru/)

версия c Docker, CI/CD используя GitHub Actions

[![Django-app workflow](https://github.com/bigbang13/foodgram-project-react/actions/workflows/main.yml/badge.svg)](https://github.com/bigbang13/foodgram-project-react/actions/workflows/main.yml)

### FoodGram
Продуктовый помощник. Публикуйте рецепты, подписывайтесь на публикации других пользователей, добавляйте понравившиеся рецепты в список «Избранное», а также, перед походом в магазин, сможете скачачть список продуктов для приготовления одного или нескольких выбранных блюд.

Данный проект запущен для ознакомления на [сервере](http://51.250.29.50).

## Как запустить проект на локальной машине:

1. Установите [Docker](https://www.docker.com/get-started)
2. Клонируйте репозиторий и перейдите в него в командной строке:
```
git clone https://github.com/bigbang13/foodgram-project-react.git
cd foodgram-project-react
```
3. Cоздайте и активируйте виртуальное окружение:
```
python -m venv venv
source venv/bin/activate
```
4. Установите зависимости из файла requirements.txt:
```
python -m pip install --upgrade pip
pip install -r requirements.txt
```
4. Создайте в каталоге ```/backend``` файл ```.env``` с переменными
```python
    SECRET_KEY=#b15&t^l36u-_btw5uq$tgkb+p_-+pdvcyd!ygcu=nh&hhyz%2
    DJANGO_DEBUG=False
    DB_ENGINE=django.db.backends.postgresql
    DB_NAME=YOUR_DB_NAME # имя базы данных
    DB_HOST=db # название контейнера с БД
    DB_PORT=5432 # порт для подключения к БД
    POSTGRES_USER=YOUR_USER_LOGIN # логин для подключения к базе данных
    POSTGRES_PASSWORD=YOUR_DB_PWD # пароль для подключения к БД
    HOST=YOUR_SERVICE_IP
```
5. Подготовим Docker образ. Перейдем в папку ```/backend``` и выполним:
```
docker build -t foodgram .
```
6. Соберем контейнеры
```
docker-compose up -d
```
7. Проверим, что запустилось 3 контейнера
```
docker-compose ps
```
8. Сделаем миграции, создадим суперпользователя и соберем статику:
```
docker-compose exec backend python manage.py makemigrations
docker-compose exec backend python manage.py migrate
docker-compose exec backend python manage.py createsuperuser
docker-compose exec backend python manage.py collectstatic --no-input 
```

## Как запустить проект на удаленном сервере:

1. Подготовка удаленного сервера
   - Остановите службу nginx
   ```
   python sudo systemctl stop nginx
   ```
   - Установите Docker и docker-compose
   ```
   python sudo apt-get update
   python sudo apt-get install docker.io docker-ce docker-ce-cli containerd.io docker-compose-plugin
   ```
   - Скопируйте файлы docker-compose.yaml и nginx/default.conf на сервер
   ```
   scp ./<FILENAME> <USER>@<HOST>:/home/<USER>/
   ```
2. Добавьте в Secrets GitHub Actions переменные окружения
   
   - SECRET_KEY - для settings Django
   - DOCKER_PASSWORD, DOCKER_USERNAME - для загрузки и скачивания образа с DockerHub
   - USER, HOST, PASSPHRASE, SSH_KEY - для подключения к удаленному серверу
   - DB_ENGINE, DB_NAME, POSTGRES_USER, POSTGRES_PASSWORD, DB_HOST, DB_PORT - для работы базы данных
   - TELEGRAM_TO, TELEGRAM_TOKEN - для отправки сообщений в Telegram

3. Развертывание приложения
   
     При пуше в ветку main автоматически запускаются тесты, при их успешном прохождении обновленный образ загружается на DockerHub, после чего
   осуществляется деплой на сервер.
   - Заходим на сервер
   ```
   ssh <USER>@<HOST>
   ```
   - Создаем суперпользователя
   ```
   sudo docker-compose exec web python manage.py createsuperuser
   ```

## Технологии
- Python 3.7
- Django 2.2.16
- Django REST Framework 3.12.4
- Docker 20.10.12

### Автор

_Рябов В.С._
_email: ryabov.v.s@yandex.ru_
_github: https://github.com/bigbang13_
