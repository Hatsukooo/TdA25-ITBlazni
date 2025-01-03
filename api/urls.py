from django.urls import path
from .views import game_list, game_detail, apicko

urlpatterns = [
    path('api', apicko, name='apicko'),  
    path('api/v1/games', game_list, name='game_list'),  
    path('api/v1/games/<uuid:pk>', game_detail, name='game_detail'), 
]