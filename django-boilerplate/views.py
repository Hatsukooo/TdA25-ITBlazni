from django.shortcuts import render
from django.views.generic import TemplateView
from api.models import Game

class page(TemplateView):
    template_name = 'main.html'

class aboutus(TemplateView):
    template_name = 'aboutus.html'

class game_list(TemplateView):
    template_name = 'game_list.html'

class game(TemplateView):
    template_name = 'game.html'
    
    def get(self, request, *args, **kwargs):
        try:
            game_obj = Game.objects.get(uuid=kwargs.get('pk'))
            return render(request, self.template_name, {'game': game_obj})
        except Game.DoesNotExist:
            return render(request, '404.html', status=404)