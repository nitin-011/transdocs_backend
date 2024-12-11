from flask import Blueprint, request, jsonify
from datetime import datetime

# Create a Blueprint for reminders
reminder_bp = Blueprint('reminder_bp', __name__)

# In-memory storage for reminders (use a database in production)
reminders = []

@reminder_bp.route('/add_reminder', methods=['POST'])
def add_reminder():
    try:
        data = request.json
        title = data.get('title')
        date = data.get('date')  # Format: YYYY-MM-DD
        time = data.get('time')  # Format: HH:MM
        toggle = data.get('toggle')  # Boolean (True/False)

        # Validate date and time
        reminder_datetime = datetime.strptime(f"{date} {time}", "%Y-%m-%d %H:%M")

        # Create a new reminder object
        new_reminder = {
            'id': len(reminders) + 1,
            'title': title,
            'date': date,
            'time': time,
            'toggle': toggle,
            'datetime': reminder_datetime
        }
        reminders.append(new_reminder)
        return jsonify({'message': 'Reminder added successfully!', 'reminder': new_reminder}), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 400

@reminder_bp.route('/get_reminders', methods=['GET'])
def get_reminders():
    return jsonify(reminders), 200

@reminder_bp.route('/toggle_reminder/<int:reminder_id>', methods=['PATCH'])
def toggle_reminder(reminder_id):
    for reminder in reminders:
        if reminder['id'] == reminder_id:
            reminder['toggle'] = not reminder['toggle']
            return jsonify({'message': 'Reminder toggled successfully!', 'reminder': reminder}), 200
    return jsonify({'error': 'Reminder not found!'}), 404
