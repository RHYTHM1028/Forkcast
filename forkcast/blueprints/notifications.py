"""
Notifications Blueprint - User notification management.

This blueprint handles:
    - Notifications page view
    - Notification CRUD operations
    - Unread count tracking
"""

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
    """Get notifications for the logged-in user."""
    user_id = session['user_id']
    with get_db_cursor() as cur:
        cur.execute('''
            SELECT * FROM notifications 
            WHERE user_id = %s 
            ORDER BY created_at DESC
            LIMIT 50
        ''', (user_id,))
        notifications_list = cur.fetchall()
    return jsonify([dict(n) for n in notifications_list] if notifications_list else [])


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
