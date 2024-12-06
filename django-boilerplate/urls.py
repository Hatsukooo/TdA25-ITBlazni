from . import views
from django.urls import include, path
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)

urlpatterns = [
    path('', views.page.as_view(), name='vectorlaunch'),
    path('todo/', views.todo.as_view(), name='todo'),
    path('api/', views.api_view, name='api'),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]
