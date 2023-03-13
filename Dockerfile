FROM python:3.7-slim
COPY requirements.txt /app
RUN pip3 install -r /app/requirements.txt --no-cache-dir
COPY . /app
WORKDIR /app
CMD ["gunicorn", "api_yamdb.wsgi:application", "--bind", "0:8000" ]
LABEL author='diana187.ami@yandex.ru' version=2.1.1