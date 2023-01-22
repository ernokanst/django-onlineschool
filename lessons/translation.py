from modeltranslation.translator import translator, TranslationOptions
import simple_history
from .models import Lesson

class LessonTranslationOptions(TranslationOptions):
    fields = ('lesson_name', 'lesson_desc')

translator.register(Lesson, LessonTranslationOptions)
simple_history.register(Lesson, inherit=True)