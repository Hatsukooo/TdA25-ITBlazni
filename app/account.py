 
import os
from flask import Blueprint, request, jsonify, session
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from .db import get_db

account_bp = Blueprint('account_bp', __name__)

UPLOAD_FOLDER = "static/profile_pictures"
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@account_bp.route('/profile', methods=['GET'])
def get_profile():
    if "user_id" not in session:
        return jsonify({"error": "Unauthorized"}), 401

    db = get_db()
    user = db.execute("SELECT id, username, email, profile_picture FROM users WHERE id = ?", (session["user_id"],)).fetchone()

    return jsonify(dict(user)), 200

@account_bp.route('/profile/update', methods=['POST'])
def update_profile():
    if "user_id" not in session:
        return jsonify({"error": "Unauthorized"}), 401

    data = request.json
    new_username = data.get("username")
    new_email = data.get("email")
    
    if not new_username or not new_email:
        return jsonify({"error": "Username and email are required"}), 400

    db = get_db()
    try:
        db.execute("UPDATE users SET username = ?, email = ? WHERE id = ?", (new_username, new_email, session["user_id"]))
        db.commit()
    except Exception as e:
        return jsonify({"error": str(e)}), 400

    session["username"] = new_username
    return jsonify({"message": "Profile updated successfully"}), 200

@account_bp.route('/profile/change-password', methods=['POST'])
def change_password():
    if "user_id" not in session:
        return jsonify({"error": "Unauthorized"}), 401

    data = request.json
    current_password = data.get("current_password")
    new_password = data.get("new_password")

    if not current_password or not new_password:
        return jsonify({"error": "Both passwords are required"}), 400

    db = get_db()
    user = db.execute("SELECT password_hash FROM users WHERE id = ?", (session["user_id"],)).fetchone()

    if not check_password_hash(user["password_hash"], current_password):
        return jsonify({"error": "Incorrect current password"}), 403

    new_password_hash = generate_password_hash(new_password)
    db.execute("UPDATE users SET password_hash = ? WHERE id = ?", (new_password_hash, session["user_id"]))
    db.commit()

    return jsonify({"message": "Password updated successfully"}), 200

@account_bp.route('/profile/upload-icon', methods=['POST'])
def upload_icon():
    if "user_id" not in session:
        return jsonify({"error": "Unauthorized"}), 401

    if "file" not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files["file"]

    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(file_path)

        db = get_db()
        db.execute("UPDATE users SET profile_picture = ? WHERE id = ?", (filename, session["user_id"]))
        db.commit()

        return jsonify({"message": "Profile picture updated successfully"}), 200

    return jsonify({"error": "Invalid file type"}), 400
