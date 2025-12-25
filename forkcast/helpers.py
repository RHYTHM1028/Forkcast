"""
Helper functions and decorators for Forkcast application.
"""

from functools import wraps
from flask import session, redirect, url_for, flash, current_app

from .models import get_db_cursor


def login_required(f):
    """Decorator to require login for routes."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to access this page.', 'error')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function


def get_current_user():
    """Get current logged-in user from database."""
    if 'user_id' not in session:
        return None
    with get_db_cursor() as cur:
        cur.execute('SELECT * FROM users WHERE id = %s', (session['user_id'],))
        return cur.fetchone()


def allowed_file(filename):
    """Check if file extension is allowed."""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']
