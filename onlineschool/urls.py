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
from rest_framework import routers, serializers, viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.response import Response

# Serializers define the API representation.
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'is_staff']
class LessonSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Lesson
        fields = ['lesson_name', 'lesson_desc', 'author', 'pub_date', 'image']

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
    
    def get_queryset(self):
        queryset = Lesson.objects.all()
        username = self.request.query_params.get('username')
        if username is not None:
            queryset = queryset.filter(author__username=username)
        return queryset
    
    @action(methods=['GET'], detail=False)
    def get_lesson_stats(self, request, **kwargs):
        lessons = Lesson.objects.all()
        data = dict()
        data['lessons_count'] = lessons.count()
        data['new_lessons'] = len([l for l in lessons if l.was_published_recently()])
        for u in User.objects.all():
            data['lessons_by_' + u.username] = 0
            for l in lessons:
                if l.author == u:
                    data['lessons_by_' + u.username] += 1
        return Response(data)    

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
