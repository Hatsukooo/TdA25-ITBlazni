from django.urls import path
from . import views

urlpatterns = [
    path('', views.apicko, name='apicko'),
    path('games/', views.create_game, name='game_list'),
    path('games/<uuid:pk>/', views.game_detail, name='game_detail'), 
]