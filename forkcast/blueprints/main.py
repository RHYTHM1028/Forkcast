"""
Main Blueprint - Public pages and general navigation.

This blueprint handles:
    - Landing page (index)
    - Home page
    - Logged-in home/dashboard
    - Favicon
"""

from flask import Blueprint, render_template, redirect, url_for, session, send_from_directory, current_app
import os

from ..helpers import login_required, get_current_user

# Create the blueprint
main_bp = Blueprint(
    'main',
    __name__,
    template_folder='../templates'
)


@main_bp.route('/')
def index():
    """
    Landing page.
    Redirects to logged-in home if user is authenticated.
    """
    if 'user_id' in session:
        return redirect(url_for('main.logged_in_home'))
    return render_template('Home.html')


@main_bp.route('/home')
def home():
    """
    Home page.
    Redirects to logged-in home if user is authenticated.
    """
    if 'user_id' in session:
        return redirect(url_for('main.logged_in_home'))
    return render_template('Home.html')


@main_bp.route('/logged-in-home')
@login_required
def logged_in_home():
    """
    Dashboard for logged-in users.
    Shows personalized content and quick access to features.
    """
    user = get_current_user()
    return render_template('logged_in_home.html', user=user)


@main_bp.route('/favicon.ico')
def favicon():
    """Serve favicon."""
    return send_from_directory(
        os.path.join(current_app.root_path, 'static', 'images'),
        'logo.png',
        mimetype='image/png'
    )
