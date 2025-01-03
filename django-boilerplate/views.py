from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import JsonResponse

class page(TemplateView):
    template_name = 'main.html'
class game(TemplateView):
    template_name = 'game.html'
class aboutus(TemplateView):
    template_name = 'aboutus.html'

class game_list(TemplateView):
    template_name = 'game_list.html'