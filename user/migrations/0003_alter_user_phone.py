# Generated by Django 3.2.16 on 2023-01-01 10:47

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_alter_user_is_staff'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='phone',
            field=models.CharField(max_length=12, unique=True, validators=[django.core.validators.RegexValidator(regex='^01([0|1|6|7|8|9]?)-?([0-9]{3,4})-?([0-9]{4})$')]),
        ),
    ]
