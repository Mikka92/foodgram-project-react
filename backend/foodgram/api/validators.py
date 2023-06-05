import re
from datetime import datetime

from rest_framework.exceptions import ValidationError


def validate_ingredient(value):
    if not value:
        raise ValidationError(
            'Нужно добавить ингридиент.'
        )
    if value['amount'] <= 0:
        raise ValidationError(
            'Количество должно быть больше 0!'
        )
    return value


def validate_date(value):
    try:
        date = datetime.strptime(value, '%Y-%m-%d')
    except ValueError:
        raise ValidationError(
            'Некорректный формат даты! Используйте формат ГГГГ-ММ-ДД.'
        )
    if date > datetime.now():
        raise ValidationError(
            'Дата не может быть в будущем!'
        )
    return value


def validate_cooking_time(value):
    if value <= 0:
        raise ValidationError(
            'Время приготовления должно быть не менее 1 минуты!'
        )
    if value >= 32767:
        raise ValidationError(
            'Время приготовления должно быть не более 32767 минут!'
        )
    return value


def validate_hex_color(value):
    if not re.match(
        r'^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$', value
    ):
        raise ValidationError(
            'Неверный формат HEX цвета!'
        )
    return value
