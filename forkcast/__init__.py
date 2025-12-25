"""
Forkcast - Recipe Sharing Application

This package contains the Flask application for Forkcast,
a recipe sharing and meal planning platform.

The application uses Flask Blueprints for modular organization:
    - main: Public pages and navigation
    - auth: Authentication (login, signup, logout)
    - profile: User profile management
    - recipes: Recipe viewing and management
    - api: RESTful API endpoints
    - calendar: Meal planning calendar
    - calorie_tracker: Calorie tracking
    - shopping_list: Shopping list management
    - notifications: User notifications
"""

from flask import Flask
import os

from .config import config


def create_app(config_name='default'):
    """
    Application factory pattern.
    
    Creates and configures the Flask application with all
    blueprints registered and extensions initialized.
    
    Args:
        config_name: Configuration to use ('development', 'production', 'testing')
    
    Returns:
        Flask application instance
    """
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    # Ensure upload directories exist
    os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], 'recipes'), exist_ok=True)
    os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], 'profiles'), exist_ok=True)
    
    # Register blueprints from the new modular structure
    from .blueprints import (
        main_bp,
        auth_bp,
        profile_bp,
        recipes_bp,
        api_bp,
        calendar_bp,
        calorie_tracker_bp,
        shopping_list_bp,
        notifications_bp,
        dashboard_bp
    )
    
    # Core blueprints (no prefix)
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(profile_bp)
    app.register_blueprint(recipes_bp)
    
    # API blueprint (already has /api prefix in its definition)
    app.register_blueprint(api_bp)
    
    # Feature blueprints (each has its own url_prefix)
    app.register_blueprint(calendar_bp)
    app.register_blueprint(calorie_tracker_bp)
    app.register_blueprint(shopping_list_bp)
    app.register_blueprint(notifications_bp)
    app.register_blueprint(dashboard_bp)
    
    # Error handlers
    @app.errorhandler(404)
    def page_not_found(e):
        from flask import request, jsonify
        if request.path.startswith('/api/'):
            return jsonify({'error': 'Not found', 'message': str(e)}), 404
        return e
    
    @app.errorhandler(500)
    def internal_server_error(e):
        from flask import request, jsonify
        if request.path.startswith('/api/'):
            return jsonify({'error': 'Internal server error', 'message': str(e)}), 500
        return e
    
    return app
