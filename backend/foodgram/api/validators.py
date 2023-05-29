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


def validate_cooking_time(value):
    if value < 1:
        raise ValidationError(
            'Время приготовления должно быть не менее 1 минуты.'
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
