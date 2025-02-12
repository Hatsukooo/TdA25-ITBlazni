# app/games.py
import json
import uuid
from datetime import datetime, timedelta
from flask import Blueprint, request, jsonify
from . import db
from .game_logic import classify_game_state, get_empty_board

game_bp = Blueprint('game_bp', __name__)

@game_bp.route('/api', methods=['GET'])
def apicko():
    return jsonify({"organization": "Student Cyber Games"}), 200

@game_bp.route('/api/v1/games', methods=['GET', 'POST'])
def game_list():
    conn = db.get_db()

    if request.method == 'GET':
        name = request.args.get('name', '').strip()
        difficulty = request.args.get('difficulty', '').strip()
        updated = request.args.get('updated', '').strip()

        rows = db.get_all_games(conn)
        games = [dict(r) for r in rows]

        if name:
            games = [g for g in games if name.lower() in g['name'].lower()]
        if difficulty:
            games = [g for g in games if g['difficulty'].lower() == difficulty.lower()]

        if updated:
            now = datetime.utcnow()
            if updated == '24h':
                threshold = now - timedelta(hours=24)
            elif updated == '7d':
                threshold = now - timedelta(days=7)
            elif updated == '1m':
                threshold = now - timedelta(days=30)
            elif updated == '3m':
                threshold = now - timedelta(days=90)
            else:
                threshold = None

            if threshold:
                def is_recent(game):
                    return datetime.fromisoformat(game['updatedAt']) >= threshold
                games = [g for g in games if is_recent(g)]

        for g in games:
            g['board'] = json.loads(g['board'])

        return jsonify(games), 200

    elif request.method == 'POST':
        data = request.json or {}
        name = data.get("name", "Untitled")
        difficulty = data.get("difficulty", "easy")
        board = data.get("board", get_empty_board())

        try:
            game_state = classify_game_state(board)
        except ValueError as e:
            return jsonify({"error": str(e)}), 422

        new_uuid = str(uuid.uuid4())
        board_json = json.dumps(board)
        db.create_game(conn, new_uuid, name, difficulty, game_state, board_json)
        row = db.get_game_by_uuid(conn, new_uuid)
        game_dict = dict(row)
        game_dict['board'] = json.loads(game_dict['board'])

        return jsonify(game_dict), 201


@game_bp.route('/api/v1/games/<uuid:game_uuid>', methods=['GET', 'PUT', 'DELETE'])
def game_detail(game_uuid):
    conn = db.get_db()
    row = db.get_game_by_uuid(conn, str(game_uuid))
    if not row:
        return jsonify({"error": "Game not found"}), 404

    if request.method == 'GET':
        game_dict = dict(row)
        game_dict['board'] = json.loads(game_dict['board'])
        return jsonify(game_dict), 200

    elif request.method == 'PUT':
        data = request.json or {}
        existing = dict(row)
        new_name = data.get("name", existing["name"])
        new_difficulty = data.get("difficulty", existing["difficulty"])
        board = data.get("board", json.loads(existing["board"]))

        try:
            game_state = classify_game_state(board)
        except ValueError as e:
            return jsonify({"error": str(e)}), 422

        board_json = json.dumps(board)
        db.update_game(conn, str(game_uuid), new_name, new_difficulty, game_state, board_json)
        updated = db.get_game_by_uuid(conn, str(game_uuid))
        updated_dict = dict(updated)
        updated_dict['board'] = json.loads(updated_dict['board'])
        return jsonify(updated_dict), 200

    elif request.method == 'DELETE':
        db.delete_game(conn, str(game_uuid))
        return '', 204
