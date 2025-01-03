from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from api.models import Game
from django.conf import settings
from django.http import FileResponse
import os
import zipfile
import io
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

# ...existing code...

class log_viewer(TemplateView):
    template_name = 'logs.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        logs = {}
        log_files = ['app.log', 'error.log', 'security.log', 'db.log']
        
        for log_file in log_files:
            file_path = os.path.join(settings.LOGS_DIR, log_file)
            if os.path.exists(file_path):
                with open(file_path, 'r') as f:
                    logs[log_file] = f.readlines()[-100:]
        
        context['logs'] = logs
        return context

    def post(self, request, *args, **kwargs):
        action = request.POST.get('action')
        
        if action == 'clear':
            log_files = ['app.log', 'error.log', 'security.log', 'db.log']
            for log_file in log_files:
                file_path = os.path.join(settings.LOGS_DIR, log_file)
                if os.path.exists(file_path):
                    open(file_path, 'w').close()
            return redirect('logs')
            
        elif action == 'download':
            memory_file = io.BytesIO()
            with zipfile.ZipFile(memory_file, 'w') as zf:
                for root, dirs, files in os.walk(settings.LOGS_DIR):
                    for file in files:
                        if file.endswith('.log'):
                            file_path = os.path.join(root, file)
                            zf.write(file_path, os.path.basename(file_path))
            memory_file.seek(0)
            return FileResponse(
                memory_file,
                as_attachment=True,
                filename='logs.zip'
            )
        
        return redirect('log_viewer')