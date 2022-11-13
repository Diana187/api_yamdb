import datetime

from rest_framework.exceptions import ValidationError


def year_validator(value):
    if value > datetime.datetime.now().year:
        raise ValidationError(
            f'Год выпуска {value} не может быть больше текущего'
        )

