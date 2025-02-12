# app/logs.py
import os, io, zipfile
from flask import Blueprint, render_template, request, redirect, url_for, send_file

log_bp = Blueprint('log_bp', __name__)

@log_bp.route('/logs', methods=['GET', 'POST'])
def logs_viewer():
    LOGS_DIR = os.path.join(os.getcwd(), 'logs')
    log_files = ['app.log', 'error.log', 'security.log', 'db.log']
    logs = {}

    if request.method == 'POST':
        action = request.form.get('action')
        if action == 'clear':
            for log_file in log_files:
                file_path = os.path.join(LOGS_DIR, log_file)
                if os.path.exists(file_path):
                    open(file_path, 'w').close()
            return redirect(url_for('log_bp.logs_viewer'))

        elif action == 'download':
            memory_file = io.BytesIO()
            with zipfile.ZipFile(memory_file, 'w') as zf:
                for log_file in log_files:
                    file_path = os.path.join(LOGS_DIR, log_file)
                    if os.path.exists(file_path):
                        zf.write(file_path, log_file)
            memory_file.seek(0)
            return send_file(memory_file, mimetype='application/zip',
                             as_attachment=True, download_name='logs.zip')

    # GET: read logs
    for log_file in log_files:
        file_path = os.path.join(LOGS_DIR, log_file)
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as f:
                all_lines = f.readlines()
                logs[log_file] = all_lines[-100:]  # Last 100 lines

    return render_template('logs.html', logs=logs)
