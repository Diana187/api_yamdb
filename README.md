
# api_yamdb
## Описание
Backend приложения Yatube. Проект объединяет в себе функционал работы api сервисов проекта социальной сети блогеров "Yatube". View- функции реализованы с помощью вьюсетов, аутентификация пользователей через JWT-токены.

## Установка


```
git clone https://github.com/Markello93/api_final_yatube.git
```

```
cd api_final_yatube
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

Запустить проект:

```
python3 manage.py runserver
```


# Примеры

Доступ к документации представлен по ссылке


  [http://127.0.0.1:8000/redoc/](http://127.0.0.1:8000/redoc/)