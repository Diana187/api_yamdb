from csv import DictReader

from django.core.management import BaseCommand

from reviews.models import Category, Comment, Genre, Review, Title
from users.models import User

ALREDY_LOADED_ERROR_MESSAGE = """
Перед загрузкой данных из CSV-файла, удалите файл БД db.sqlite3.
Создайте миграции `python manage.py makemigrations`.
Выполните миграции `python manage.py migrate`.
"""


class Command(BaseCommand):
    help = "Загрузка данных из CSV файлов"

    def handle(self, *args, **options):

        if (
            Category.objects.exists()
            or Genre.objects.exists()
            or Title.objects.exists()
            or Review.objects.exists()
            or Comment.objects.exists()
            or User.objects.exists()
        ):
            print('в таблице Жанры уже содержатся данные.')
            print(ALREDY_LOADED_ERROR_MESSAGE)
            return

        file_path = 'static/data/users.csv'
        data_list = []
        with open(file_path, mode="r", encoding="utf-8") as file:
            reader = DictReader(file)
            self.stdout.write(f'Загрузка данных из {file_path}... ', ending='')
            for row in reader:
                data_list.append(
                    User(
                        id=row['id'],
                        username=row['username'],
                        email=row['email'],
                        role=row['role'],
                        bio=row['bio'],
                        first_name=row['first_name'],
                        last_name=row['last_name'],
                    )
                )
            User.objects.bulk_create(data_list)
        self.stdout.write(self.style.SUCCESS("OK"))

        file_path = 'static/data/category.csv'
        data_list = []
        with open(file_path, mode="r", encoding="utf-8") as file:
            reader = DictReader(file)
            self.stdout.write(f'Загрузка данных из {file_path}... ', ending='')
            for row in reader:
                data_list.append(Category(name=row['name'], slug=row['slug']))
            Category.objects.bulk_create(data_list)
        self.stdout.write(self.style.SUCCESS("OK"))

        file_path = 'static/data/genre.csv'
        data_list = []
        with open(file_path, mode="r", encoding="utf-8") as file:
            reader = DictReader(file)
            self.stdout.write(f'Загрузка данных из {file_path}... ', ending='')
            for row in reader:
                data_list.append(Genre(name=row['name'], slug=row['slug']))
            Genre.objects.bulk_create(data_list)
        self.stdout.write(self.style.SUCCESS("OK"))

        file_path = 'static/data/titles.csv'
        data_list = []
        with open(file_path, mode="r", encoding="utf-8") as file:
            reader = DictReader(file)
            self.stdout.write(f'Загрузка данных из {file_path}... ', ending='')
            for row in reader:
                data_list.append(
                    Title(
                        name=row['name'],
                        year=row['year'],
                        category_id=row['category'],
                    )
                )
            Title.objects.bulk_create(data_list)
        self.stdout.write(self.style.SUCCESS("OK"))

        file_path = 'static/data/review.csv'
        data_list = []
        with open(file_path, mode="r", encoding="utf-8") as file:
            reader = DictReader(file)
            self.stdout.write(f"Загрузка данных из {file_path}... ", ending='')
            for row in reader:
                data_list.append(
                    Review(
                        title_id=row['title_id'],
                        text=row['text'],
                        author_id=row['author'],
                        score=row['score'],
                        pub_date=row['pub_date'],
                    )
                )
            Review.objects.bulk_create(data_list)
        self.stdout.write(self.style.SUCCESS("OK"))

        file_path = 'static/data/comments.csv'
        data_list = []
        with open(file_path, mode="r", encoding="utf-8") as file:
            reader = DictReader(file)
            self.stdout.write(f"Загрузка данных из {file_path}... ", ending='')
            for row in reader:
                data_list.append(
                    Comment(
                        review_id=row['review_id'],
                        text=row['text'],
                        author_id=row['author'],
                        pub_date=row['pub_date'],
                    )
                )
            Comment.objects.bulk_create(data_list)
        self.stdout.write(self.style.SUCCESS("OK"))

        file_path = 'static/data/genre_title.csv'
        with open(file_path, mode="r", encoding="utf-8") as file:
            reader = DictReader(file)
            self.stdout.write(f"Загрузка данных из {file_path}... ", ending='')
            for row in reader:
                title_obj = Title.objects.get(id=row['title_id'])
                genre = Genre.objects.get(id=row['genre_id'])

                title_obj.genre.add(genre)
        self.stdout.write(self.style.SUCCESS("OK"))

# ============================================================================
#         file_path_list = {
#             User: 'static/data/users.csv',
#             Category: 'static/data/category.csv',
#             Genre: 'static/data/genre.csv',
#             Title: 'static/data/titles.csv',
#             Review: 'static/data/review.csv',
#             Comment: 'static/data/comment.csv',
#         }
#
#         for model, file_path in file_path_list.items():
#             with open(
#                 f'E:/ДОкументы/my_Python/api_yamdb/api_yamdb/{file_path}',
#                 mode="r", encoding="utf-8"
#             ) as file:
#                 reader = DictReader(file)
#                 self.stdout.write(
#                     f"Загрузка данных из {file_path}... ",
#                     ending=''
#                 )
#                 model.objects.bulk_create(model(**data) for data in reader)
#             self.stdout.write(self.style.SUCCESS("OK"))
