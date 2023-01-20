from django.db import models
import datetime
from django.utils import timezone

class Lesson(models.Model):
    lesson_name = models.CharField('Название урока', max_length=50)
    lesson_desc = models.TextField('Описание урока')
    pub_date = models.DateTimeField('Дата публикации')
    image = models.ImageField('Изображение', upload_to='static/lessons/', blank=True)
    
    def __str__(self):
        return self.lesson_name
    
    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now