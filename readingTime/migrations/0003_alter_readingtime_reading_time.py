# Generated by Django 3.2.16 on 2022-12-29 05:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('readingTime', '0002_readingtime_user_news'),
    ]

    operations = [
        migrations.AlterField(
            model_name='readingtime',
            name='reading_time',
            field=models.IntegerField(),
        ),
    ]
