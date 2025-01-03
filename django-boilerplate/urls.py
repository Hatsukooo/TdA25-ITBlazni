from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('api.urls')),
    path('', views.page.as_view(), name='home'),
    path('game/', views.game_list.as_view(), name='game_list'),
    path('game/<uuid:pk>/', views.game.as_view(), name='game'),
    path('aboutus/', views.aboutus.as_view(), name='aboutus'),
    path('logs/', views.log_viewer.as_view(), name='logs'),
]