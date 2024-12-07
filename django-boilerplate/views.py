from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import JsonResponse
from django.shortcuts import render

class page(TemplateView):
    template_name = 'main.html'
    
class todo(TemplateView):
    template_name = 'todo.html'    

def api_view(request):
    return JsonResponse({"organization": "Student Cyber Games"})