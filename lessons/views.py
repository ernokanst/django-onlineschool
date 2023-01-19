from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic

from .models import Lesson


class IndexView(generic.ListView):
    template_name = 'lessons/index.html'
    context_object_name = 'lesson_list'

    def get_queryset(self):
        return Lesson.objects.order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Lesson
    template_name = 'lessons/detail.html'