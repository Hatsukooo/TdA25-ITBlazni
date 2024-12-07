from . import views
from django.contrib.auth.models import User
from django.urls import path

urlpatterns = [
    path('', views.page.as_view(), name='home'),
    path('todo/', views.todo.as_view(), name='todo'),
    path('api/', views.api_view, name='api'),  
]
