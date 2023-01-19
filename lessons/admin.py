from django.contrib import admin

from .models import Lesson


class LessonAdmin(admin.ModelAdmin):
    list_display = ('lesson_name', 'lesson_desc', 'pub_date')
    list_filter = ['pub_date']
    search_fields = ['lesson_name', 'lesson_desc']

admin.site.register(Lesson, LessonAdmin)