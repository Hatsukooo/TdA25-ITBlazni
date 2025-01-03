from django.urls import path
from . import views

urlpatterns = [
    path('', views.apicko, name='apicko'),
    path('v1/games/', views.game_list, name='game_list'),
    path('v1/games/<uuid:pk>/', views.game_detail, name='game_detail'), 
]