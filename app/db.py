# app/db.py

import sqlite3
import click
from flask import current_app, g
from flask.cli import with_appcontext
from flask import current_app

def get_db():
    print("DEBUG CONFIG:", current_app.config)  # Debugging line

    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row
    return g.db


def close_db(e=None):
    db_conn = g.pop('db', None)
    if db_conn is not None:
        db_conn.close()

def init_db():
    db_conn = get_db()
    with current_app.open_resource('schema.sql', mode='r') as f:
        db_conn.executescript(f.read())

@click.command('init-db')
@with_appcontext
def init_db_command():
    """ CLI command: flask init-db """
    init_db()
    click.echo("Initialized the database.")

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)

# "CRUD" helpers for the 'games' table
def create_game(db_conn, uuid_str, name, difficulty, game_state, board_json):
    now_str = "2025-01-01T00:00:00Z"  # or datetime.utcnow().isoformat()
    db_conn.execute("""
        INSERT INTO games (uuid, createdAt, updatedAt, name, difficulty, gameState, board)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (uuid_str, now_str, now_str, name, difficulty, game_state, board_json))
    db_conn.commit()

def get_all_games(db_conn):
    return db_conn.execute("SELECT * FROM games").fetchall()

def get_game_by_uuid(db_conn, uuid_str):
    return db_conn.execute("SELECT * FROM games WHERE uuid=?", (uuid_str,)).fetchone()

def update_game(db_conn, uuid_str, name, difficulty, game_state, board_json):
    now_str = "2025-01-01T00:00:00Z"
    db_conn.execute("""
        UPDATE games
           SET name=?, difficulty=?, gameState=?, board=?, updatedAt=?
         WHERE uuid=?
    """, (name, difficulty, game_state, board_json, now_str, uuid_str))
    db_conn.commit()

def delete_game(db_conn, uuid_str):
    db_conn.execute("DELETE FROM games WHERE uuid=?", (uuid_str,))
    db_conn.commit()