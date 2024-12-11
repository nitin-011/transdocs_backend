import os
from flask import Blueprint, jsonify, request

# Blueprint for the recycle bin
recycle_bin_bp = Blueprint('recycle_bin', __name__)

# Recycle Bin folder
RECYCLE_BIN_FOLDER = os.path.abspath('recycle_bin')
os.makedirs(RECYCLE_BIN_FOLDER, exist_ok=True)

# List files in the recycle bin
@recycle_bin_bp.route('/recyclebin', methods=['GET'])
def list_recycle_bin():
    files = os.listdir(RECYCLE_BIN_FOLDER)
    return jsonify({'files': files})

# Move files to recycle bin
@recycle_bin_bp.route('/move_to_recycle', methods=['POST'])
def move_to_recycle():
    data = request.get_json()
    files = data.get('files', [])
    for file in files:
        file_path = os.path.join(request.form['UPLOAD_FOLDER'], file)
        if os.path.exists(file_path):
            os.rename(file_path, os.path.join(RECYCLE_BIN_FOLDER, file))
    return jsonify({'message': 'Files moved to recycle bin successfully'})

# Restore files from recycle bin
@recycle_bin_bp.route('/restore', methods=['POST'])
def restore_from_recycle():
    data = request.get_json()
    files = data.get('files', [])
    for file in files:
        recycle_path = os.path.join(RECYCLE_BIN_FOLDER, file)
        if os.path.exists(recycle_path):
            os.rename(recycle_path, os.path.join(request.form['UPLOAD_FOLDER'], file))
    return jsonify({'message': 'Files restored successfully'})

# Delete files permanently
@recycle_bin_bp.route('/delete_permanently', methods=['POST'])
def delete_permanently():
    data = request.get_json()
    files = data.get('files', [])
    for file in files:
        file_path = os.path.join(RECYCLE_BIN_FOLDER, file)
        if os.path.exists(file_path):
            os.remove(file_path)
    return jsonify({'message': 'Files deleted permanently'})