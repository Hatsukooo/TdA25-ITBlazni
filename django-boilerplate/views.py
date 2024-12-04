from django.shortcuts import render
from django.views.generic import TemplateView

class stranka(TemplateView):
    template_name = 'main.html'