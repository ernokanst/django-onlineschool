from django.db import models

class Lesson(models.Model):
    lesson_name = models.CharField('Название урока', max_length=50)
    lesson_desc = models.TextField('Описание урока')
    pub_date = models.DateTimeField('Дата публикации')
    image = models.FileField('Изображение', upload_to='static/')
    
    def __str__(self):
        return self.lesson_name