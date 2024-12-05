from . import views
from django.urls import path

urlpatterns = [
    path('', views.page.as_view(), name='vectorlaunch'),
    path('todo/', views.todo.as_view(), name='todo'),
    path('api/', views.api_view, name='api'),
]
