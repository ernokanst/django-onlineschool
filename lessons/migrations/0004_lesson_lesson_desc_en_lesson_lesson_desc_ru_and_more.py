# Generated by Django 4.1.5 on 2023-01-21 17:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lessons', '0003_historicallesson'),
    ]

    operations = [
        migrations.AddField(
            model_name='lesson',
            name='lesson_desc_en',
            field=models.TextField(null=True, verbose_name='Описание урока'),
        ),
        migrations.AddField(
            model_name='lesson',
            name='lesson_desc_ru',
            field=models.TextField(null=True, verbose_name='Описание урока'),
        ),
        migrations.AddField(
            model_name='lesson',
            name='lesson_name_en',
            field=models.CharField(max_length=50, null=True, verbose_name='Название урока'),
        ),
        migrations.AddField(
            model_name='lesson',
            name='lesson_name_ru',
            field=models.CharField(max_length=50, null=True, verbose_name='Название урока'),
        ),
    ]
