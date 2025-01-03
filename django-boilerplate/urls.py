from . import views
from django.urls import path, include

urlpatterns = [
    path('', views.page.as_view(), name='home'),
    path('game/', views.game.as_view(), name='game'),
    path('aboutus/', views.aboutus.as_view(), name='aboutus'),
    path('api/', include('api.urls'), name='api'),
    path('game-list/', views.game_list.as_view(), name='game_list'),
]