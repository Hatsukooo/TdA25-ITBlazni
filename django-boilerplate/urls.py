from . import views
from django.urls import path

urlpatterns = [
    path('', views.page.as_view(), name='vectorlaunch'),
]
