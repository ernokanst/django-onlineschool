# Generated by Django 4.1.5 on 2023-01-21 17:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lessons', '0004_lesson_lesson_desc_en_lesson_lesson_desc_ru_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='HistoricalLesson',
        ),
    ]
