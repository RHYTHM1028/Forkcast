"""
Calorie Tracker Blueprint - Calorie tracking features.

This blueprint handles:
    - Calorie tracker page view
    - Calorie log CRUD operations
"""

from flask import Blueprint, render_template, request, jsonify, session

from ..helpers import login_required, get_current_user
from ..models import get_db_cursor

# Create the blueprint
calorie_tracker_bp = Blueprint(
    'calorie_tracker',
    __name__,
    template_folder='../templates',
    url_prefix='/calorie-tracker'
)


@calorie_tracker_bp.route('/')
@login_required
def calorie_tracker():
    """Display calorie tracking page."""
    user = get_current_user()
    return render_template('calorie_tracker.html', user=user)


@calorie_tracker_bp.route('/api/logs', methods=['GET'])
@login_required
def get_calorie_logs():
    """Get calorie logs for the logged-in user."""
    user_id = session['user_id']
    date = request.args.get('date')
    
    query = '''
        SELECT cl.*, r.name as recipe_name, r.calories as recipe_calories
        FROM calorie_logs cl
        LEFT JOIN recipes r ON cl.recipe_id = r.id
        WHERE cl.user_id = %s
    '''
    params = [user_id]
    
    if date:
        query += ' AND DATE(cl.log_date) = %s'
        params.append(date)
    
    query += ' ORDER BY cl.log_date DESC'
    
    with get_db_cursor() as cur:
        cur.execute(query, params)
        logs = cur.fetchall()
    
    return jsonify([dict(log) for log in logs] if logs else [])


@calorie_tracker_bp.route('/api/logs', methods=['POST'])
@login_required
def add_calorie_log():
    """Add a calorie log entry."""
    data = request.get_json()
    user_id = session['user_id']
    
    with get_db_cursor(commit=True) as cur:
        cur.execute('''
            INSERT INTO calorie_logs (user_id, recipe_id, calories, meal_type, log_date, notes)
            VALUES (%s, %s, %s, %s, COALESCE(%s, CURRENT_DATE), %s)
            RETURNING id
        ''', (user_id, data.get('recipe_id'), data.get('calories'),
              data.get('meal_type'), data.get('log_date'), data.get('notes')))
        log_id = cur.fetchone()['id']
    
    return jsonify({'success': True, 'log_id': log_id})


@calorie_tracker_bp.route('/api/logs/<int:log_id>', methods=['DELETE'])
@login_required
def delete_calorie_log(log_id):
    """Delete a calorie log entry."""
    user_id = session['user_id']
    with get_db_cursor(commit=True) as cur:
        cur.execute('''
            DELETE FROM calorie_logs 
            WHERE id = %s AND user_id = %s
        ''', (log_id, user_id))
    return jsonify({'success': True})
