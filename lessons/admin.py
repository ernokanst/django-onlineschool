from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin
from modeltranslation.admin import TranslationAdmin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from .models import Lesson


class LessonAdmin(SimpleHistoryAdmin):
    list_display = ('lesson_name', 'lesson_desc', 'pub_date')
    history_list_display = ['changed_fields']
    list_filter = ['pub_date']
    search_fields = ['lesson_name', 'lesson_desc']
    def changed_fields(self, obj):
        if obj.prev_record:
            delta = obj.diff_against(obj.prev_record)
            return delta.changed_fields
        return None

class TranslatedLessonAdmin(LessonAdmin, TranslationAdmin):
    pass

class LessonResource(resources.ModelResource):
    class Meta:
        model = Lesson

class LessonExportAdmin(TranslatedLessonAdmin, ImportExportModelAdmin):
    resource_classes = [LessonResource]

admin.site.register(Lesson, LessonExportAdmin)