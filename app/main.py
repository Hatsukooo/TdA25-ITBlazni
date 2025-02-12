# app/main.py
from flask import Blueprint, render_template

main_bp = Blueprint('main_bp', __name__)

@main_bp.route('/')
def home():
    return render_template('main.html')

@main_bp.route('/about')
def about():
    return render_template('aboutus.html')

@main_bp.route('/game_list')
def game_list_page():
    return render_template('game_list.html')

@main_bp.route('/game/<uuid:gid>')
def game_page(gid):
    return render_template('game.html', game={"name": f"Game {gid}"})
