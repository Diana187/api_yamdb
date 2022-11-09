# api_yamdb
## Описание
Backend приложения YamDB. 
Проект объединяет в себе функционал работы api сервисов проекта для публикации произведений,
отзывов и комментариев к ним. 
View- функции реализованы с помощью вьюсетов, аутентификация пользователей через JWT-токены.

## Установка
```
https://github.com/Diana187/api_yamdb.git
```
```
cd api_yamdb
```
Cоздать и активировать виртуальное окружение:
```
python3 -m venv env
```
```
source env/bin/activate
```
Установить зависимости из файла requirements.txt:
```
python3 -m pip install --upgrade pip
```
```
pip install -r requirements.txt
```
Выполнить миграции:
```
python3 manage.py migrate
```
Выполнить импорт данных в базу данных (при необходимости):
```
python3 manage.py load_data_from_csv
```
Запустить проект:
```
python3 manage.py runserver
```

# Примеры
Доступ к документации API представлен по ссылке:
[http://127.0.0.1:8000/redoc/](http://127.0.0.1:8000/redoc/)