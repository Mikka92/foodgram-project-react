# Generated by Django 3.2.19 on 2023-05-29 05:21

import api.validators
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='recipe',
            name='pub_date',
        ),
        migrations.AddField(
            model_name='recipe',
            name='date',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, validators=[api.validators.validate_date], verbose_name='Дата публикации'),
            preserve_default=False,
        ),
    ]
