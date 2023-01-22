"""onlineschool URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path, re_path
from django.contrib.auth.models import User
from lessons.models import Lesson
from rest_framework import routers, serializers, viewsets, filters, status
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import translation, timezone
from rest_framework.validators import UniqueValidator
from django.db.models import Q

# Serializers define the API representation.
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'is_staff']
class LessonSerializer(serializers.HyperlinkedModelSerializer):
    lesson_name = serializers.CharField(label='Название урока', max_length=50, validators=[UniqueValidator(queryset=Lesson.objects.all(), message="Lesson name must be unique")])
    image = serializers.URLField(label='Изображение')
    class Meta:
        model = Lesson
        fields = ['id', 'lesson_name', 'lesson_desc', 'author', 'pub_date', 'image']
    def validate_author(self, author):
        if not author.is_staff:
            raise serializers.ValidationError("Only staff members can author lessons.")
        return author

# ViewSets define the view behavior.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
class LessonViewSet(viewsets.ModelViewSet):
    serializer_class = LessonSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    filterset_fields = ['author']
    search_fields = ['lesson_name', 'lesson_desc']
    ordering_fields = ['lesson_name', 'pub_date']
    
    def initial(self, request, *args, **kwargs):
        language = kwargs.get('lang')
        translation.activate(language)
        super(LessonViewSet, self).initial(request, *args, **kwargs)    
    
    def get_queryset(self):
        queryset = Lesson.objects.filter(Q(pub_date__lte=timezone.now()))
        username = self.request.query_params.get('username')
        if username is not None:
            queryset = queryset.filter(author__username=username)
        return queryset
    
    @action(methods=['GET'], detail=False, name='Получить статистику уроков')
    def get_lesson_stats(self, request, **kwargs):
        lessons = Lesson.objects.all()
        data = dict()
        data['lessons_count'] = lessons.count()
        data['new_lessons'] = len([l for l in lessons if l.was_published_recently()])
        for u in User.objects.all():
            if u.is_staff:
                data['lessons_by_' + u.username] = 0
                for l in lessons:
                    if l.author == u:
                        data['lessons_by_' + u.username] += 1
        return Response(data)
    
    @action(methods=['POST'], detail=True, name='Добавить внешнее изображение')
    def add_external_image(self, request, **kwargs):
        lesson = self.get_object()
        externalimage = request.data['image']
        if externalimage:
            lesson.image = externalimage
            lesson.save()
        return Response()

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'lessons', LessonViewSet, basename='lessons')

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    re_path('(?P<lang>(ru|en))/', include(router.urls)),
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('', include('lessons.urls')),
    path('admin/', admin.site.urls),
]
