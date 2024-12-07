from . import views
from django.urls import path, include

urlpatterns = [
    path('', views.page.as_view(), name='home'),
    path('game/', views.game.as_view(), name='game'),
    path('aboutus/', views.aboutus.as_view(), name='aboutus'),
    path('api/', views.api_view, name='api'),
]
