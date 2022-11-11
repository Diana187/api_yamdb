# api_yamdb
## Описание
Backend приложения YamDB.

Проект объединяет в себе функционал работы api сервисов проекта для публикации произведений,
отзывов и комментариев к ним. 
View-функции реализованы с помощью вьюсетов, аутентификация пользователей через JWT-токены.

## ⚙️ Технологии:

- ![image](https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=blue) (3.7.13)
- ![image](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=green) (3.2.16)
- ![image](https://img.shields.io/badge/django%20rest-ff1709?style=for-the-badge&logo=django&logoColor=white) (3.12.4)

## Установка

Клонировать репозиторий и перейти в него в командной строке:
```
git clone https://github.com/Diana187/api_yamdb.git
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
