from datetime import timezone

from rest_framework.exceptions import ValidationError


def year_validator(value):
    if value < 1900 or value > timezone.localtime(timezone.now()).year:
        raise ValidationError(
            "Год не должен быть больше текущего",
            params={"value": value},
        )
