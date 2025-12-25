"""
Notifications Blueprint - User notification management.

This blueprint handles:
    - Notifications page view
    - Notification CRUD operations
    - Unread count tracking
    - Meal reminder settings
    - Real-time notification polling
"""

import json
from datetime import datetime, timedelta
from flask import Blueprint, render_template, request, jsonify, session

from ..helpers import login_required, get_current_user
from ..models import get_db_cursor

# Create the blueprint
notifications_bp = Blueprint(
    'notifications',
    __name__,
    template_folder='../templates',
    url_prefix='/notifications'
)


@notifications_bp.route('/')
@login_required
def notifications():
    """Display notifications page."""
    user = get_current_user()
    return render_template('notification.html', user=user)


@notifications_bp.route('/api/list', methods=['GET'])
@login_required
def get_notifications():
    """Get notifications for the logged-in user with pagination and filtering."""
    user_id = session['user_id']
    notification_type = request.args.get('type', 'all')
    unread_only = request.args.get('unread', 'false') == 'true'
    limit = min(int(request.args.get('limit', 50)), 100)
    offset = int(request.args.get('offset', 0))
    
    query = '''
        SELECT n.*, 
               u.username as from_username, 
               u.full_name as from_full_name,
               u.profile_image as from_profile_image
        FROM notifications n
        LEFT JOIN users u ON n.from_user_id = u.id
        WHERE n.user_id = %s
    '''
    params = [user_id]
    
    if notification_type != 'all':
        query += ' AND n.type = %s'
        params.append(notification_type)
    
    if unread_only:
        query += ' AND n.is_read = FALSE'
    
    query += ' ORDER BY n.created_at DESC LIMIT %s OFFSET %s'
    params.extend([limit, offset])
    
    with get_db_cursor() as cur:
        cur.execute(query, tuple(params))
        notifications_list = cur.fetchall()
        
        # Convert to list of dicts with proper datetime formatting
        result = []
        for n in notifications_list:
            notif = dict(n)
            if notif.get('created_at'):
                notif['created_at'] = notif['created_at'].isoformat()
            if notif.get('action_data') and isinstance(notif['action_data'], str):
                try:
                    notif['action_data'] = json.loads(notif['action_data'])
                except:
                    pass
            result.append(notif)
    
    return jsonify(result)


@notifications_bp.route('/api/<int:notification_id>/read', methods=['PUT'])
@login_required
def mark_notification_read(notification_id):
    """Mark a notification as read."""
    user_id = session['user_id']
    with get_db_cursor(commit=True) as cur:
        cur.execute('''
            UPDATE notifications 
            SET is_read = TRUE
            WHERE id = %s AND user_id = %s
        ''', (notification_id, user_id))
    return jsonify({'success': True})


@notifications_bp.route('/api/read-all', methods=['PUT'])
@login_required
def mark_all_notifications_read():
    """Mark all notifications as read."""
    user_id = session['user_id']
    with get_db_cursor(commit=True) as cur:
        cur.execute('''
            UPDATE notifications 
            SET is_read = TRUE
            WHERE user_id = %s AND is_read = FALSE
        ''', (user_id,))
    return jsonify({'success': True})


@notifications_bp.route('/api/<int:notification_id>', methods=['DELETE'])
@login_required
def delete_notification(notification_id):
    """Delete a specific notification."""
    user_id = session['user_id']
    with get_db_cursor(commit=True) as cur:
        cur.execute('''
            DELETE FROM notifications 
            WHERE id = %s AND user_id = %s
        ''', (notification_id, user_id))
    return jsonify({'success': True})


@notifications_bp.route('/api/clear-all', methods=['DELETE'])
@login_required
def clear_all_notifications():
    """Clear all notifications for the user."""
    user_id = session['user_id']
    with get_db_cursor(commit=True) as cur:
        cur.execute('''
            DELETE FROM notifications 
            WHERE user_id = %s
        ''', (user_id,))
    return jsonify({'success': True})


@notifications_bp.route('/api/unread-count', methods=['GET'])
@login_required
def get_unread_count():
    """Get count of unread notifications."""
    user_id = session['user_id']
    with get_db_cursor() as cur:
        cur.execute('''
            SELECT COUNT(*) as count 
            FROM notifications 
            WHERE user_id = %s AND is_read = FALSE
        ''', (user_id,))
        result = cur.fetchone()
    return jsonify({'count': result['count'] if result else 0})


@notifications_bp.route('/api/stats', methods=['GET'])
@login_required
def get_notification_stats():
    """Get notification statistics."""
    user_id = session['user_id']
    today = datetime.now().date()
    
    with get_db_cursor() as cur:
        # Total notifications
        cur.execute('SELECT COUNT(*) as count FROM notifications WHERE user_id = %s', (user_id,))
        total = cur.fetchone()['count']
        
        # Unread count
        cur.execute('SELECT COUNT(*) as count FROM notifications WHERE user_id = %s AND is_read = FALSE', (user_id,))
        unread = cur.fetchone()['count']
        
        # Today's meal reminders
        cur.execute('''
            SELECT COUNT(*) as count FROM notifications 
            WHERE user_id = %s AND type = 'meal' AND DATE(created_at) = %s
        ''', (user_id, today))
        today_reminders = cur.fetchone()['count']
    
    return jsonify({
        'total': total,
        'unread': unread,
        'today_reminders': today_reminders
    })


@notifications_bp.route('/api/create-meal-reminder', methods=['POST'])
@login_required
def create_meal_reminder_api():
    """Create a meal reminder notification from client-side trigger."""
    user_id = session['user_id']
    data = request.get_json()
    
    meal_type = data.get('meal_type', 'meal')
    meal_time = data.get('meal_time', '')
    recipe_title = data.get('recipe_title')
    
    notification_id = create_meal_reminder(
        user_id=user_id,
        meal_type=meal_type,
        recipe_title=recipe_title,
        meal_time=meal_time
    )
    
    return jsonify({'success': True, 'notification_id': notification_id})


# ==================== MEAL REMINDER SETTINGS ====================

@notifications_bp.route('/api/settings', methods=['GET'])
@login_required
def get_reminder_settings():
    """Get user's meal reminder settings."""
    user_id = session['user_id']
    
    with get_db_cursor() as cur:
        cur.execute('SELECT * FROM meal_reminder_settings WHERE user_id = %s', (user_id,))
        settings = cur.fetchone()
    
    if settings:
        result = dict(settings)
        # Convert time objects to strings
        for key in ['breakfast_time', 'lunch_time', 'dinner_time', 'snack_time']:
            if result.get(key):
                result[key] = str(result[key])[:5]  # Format as HH:MM
        return jsonify(result)
    
    # Return defaults if no settings exist
    return jsonify({
        'reminders_enabled': True,
        'breakfast_time': '08:00',
        'lunch_time': '12:00',
        'dinner_time': '18:00',
        'snack_time': '15:00',
        'breakfast_reminder_minutes': 30,
        'lunch_reminder_minutes': 30,
        'dinner_reminder_minutes': 30,
        'snack_reminder_minutes': 30,
        'notify_weekly_plan': True,
        'notify_shopping_list': True,
        'notify_new_recipes': True,
        'notify_calorie_goal': True,
        'sound_enabled': True
    })


@notifications_bp.route('/api/settings', methods=['PUT'])
@login_required
def update_reminder_settings():
    """Update user's meal reminder settings."""
    user_id = session['user_id']
    data = request.get_json()
    
    with get_db_cursor(commit=True) as cur:
        cur.execute('''
            INSERT INTO meal_reminder_settings (
                user_id, reminders_enabled,
                breakfast_time, lunch_time, dinner_time, snack_time,
                breakfast_reminder_minutes, lunch_reminder_minutes, 
                dinner_reminder_minutes, snack_reminder_minutes,
                notify_weekly_plan, notify_shopping_list, 
                notify_new_recipes, notify_calorie_goal, sound_enabled,
                updated_at
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, CURRENT_TIMESTAMP)
            ON CONFLICT (user_id) DO UPDATE SET
                reminders_enabled = EXCLUDED.reminders_enabled,
                breakfast_time = EXCLUDED.breakfast_time,
                lunch_time = EXCLUDED.lunch_time,
                dinner_time = EXCLUDED.dinner_time,
                snack_time = EXCLUDED.snack_time,
                breakfast_reminder_minutes = EXCLUDED.breakfast_reminder_minutes,
                lunch_reminder_minutes = EXCLUDED.lunch_reminder_minutes,
                dinner_reminder_minutes = EXCLUDED.dinner_reminder_minutes,
                snack_reminder_minutes = EXCLUDED.snack_reminder_minutes,
                notify_weekly_plan = EXCLUDED.notify_weekly_plan,
                notify_shopping_list = EXCLUDED.notify_shopping_list,
                notify_new_recipes = EXCLUDED.notify_new_recipes,
                notify_calorie_goal = EXCLUDED.notify_calorie_goal,
                sound_enabled = EXCLUDED.sound_enabled,
                updated_at = CURRENT_TIMESTAMP
        ''', (
            user_id,
            data.get('reminders_enabled', True),
            data.get('breakfast_time', '08:00'),
            data.get('lunch_time', '12:00'),
            data.get('dinner_time', '18:00'),
            data.get('snack_time', '15:00'),
            data.get('breakfast_reminder_minutes', 30),
            data.get('lunch_reminder_minutes', 30),
            data.get('dinner_reminder_minutes', 30),
            data.get('snack_reminder_minutes', 30),
            data.get('notify_weekly_plan', True),
            data.get('notify_shopping_list', True),
            data.get('notify_new_recipes', True),
            data.get('notify_calorie_goal', True),
            data.get('sound_enabled', True)
        ))
    
    return jsonify({'success': True, 'message': 'Settings saved successfully!'})


# ==================== NOTIFICATION CREATION HELPERS ====================

def create_notification(user_id, title, message, notification_type='info', 
                       action_url=None, action_data=None, related_id=None, from_user_id=None):
    """
    Create a new notification for a user.
    
    Args:
        user_id: The user to notify
        title: Notification title
        message: Notification message
        notification_type: Type of notification (review, meal, shopping, recipe, info)
        action_url: URL to navigate to when clicked
        action_data: Additional data (stored as JSON)
        related_id: ID of related entity (recipe_id, etc.)
        from_user_id: User who triggered this notification
    """
    with get_db_cursor(commit=True) as cur:
        cur.execute('''
            INSERT INTO notifications (user_id, title, message, type, action_url, action_data, related_id, from_user_id)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING id
        ''', (
            user_id, title, message, notification_type,
            action_url,
            json.dumps(action_data) if action_data else None,
            related_id,
            from_user_id
        ))
        return cur.fetchone()['id']


def create_review_notification(recipe_owner_id, reviewer_id, recipe_id, recipe_title, rating, review_text=None):
    """Create a notification when someone reviews a recipe."""
    with get_db_cursor() as cur:
        cur.execute('SELECT username, full_name FROM users WHERE id = %s', (reviewer_id,))
        reviewer = cur.fetchone()
    
    reviewer_name = reviewer['full_name'] or reviewer['username'] if reviewer else 'Someone'
    stars = '★' * rating
    
    title = f'New Review on "{recipe_title}"'
    message = f'{reviewer_name} rated your recipe {stars}'
    if review_text:
        message += f': "{review_text[:100]}{"..." if len(review_text) > 100 else ""}"'
    
    return create_notification(
        user_id=recipe_owner_id,
        title=title,
        message=message,
        notification_type='review',
        action_url=f'/recipes?view={recipe_id}',
        action_data={'recipe_id': recipe_id, 'rating': rating},
        related_id=recipe_id,
        from_user_id=reviewer_id
    )


def create_meal_reminder(user_id, meal_type, recipe_title=None, meal_time=None):
    """Create a meal reminder notification."""
    meal_names = {
        'breakfast': 'Breakfast',
        'lunch': 'Lunch', 
        'dinner': 'Dinner',
        'snack': 'Snack'
    }
    
    title = f'{meal_names.get(meal_type, "Meal")} Reminder'
    if recipe_title:
        message = f'Time to prepare: {recipe_title}'
    else:
        message = f'It\'s almost time for {meal_names.get(meal_type, "your meal")}!'
    
    return create_notification(
        user_id=user_id,
        title=title,
        message=message,
        notification_type='meal',
        action_url='/calendar',
        action_data={'meal_type': meal_type, 'time': meal_time}
    )
