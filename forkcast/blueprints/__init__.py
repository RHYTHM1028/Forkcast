"""
Blueprints Package - Contains all Flask blueprints for the Forkcast application.

Each blueprint is organized as a separate module with its own routes.
This follows Flask best practices for modular application design.

Blueprints:
    - main: Public pages and navigation (home, index)
    - auth: Authentication (login, signup, logout)
    - profile: User profile management
    - recipes: Recipe viewing and management
    - api: RESTful API endpoints for AJAX operations
    - calendar: Meal planning calendar features
    - calorie_tracker: Calorie tracking features
    - shopping_list: Shopping list management
    - notifications: User notifications
"""

from .main import main_bp
from .auth import auth_bp
from .profile import profile_bp
from .recipes import recipes_bp
from .api import api_bp
from .calendar import calendar_bp
from .calorie_tracker import calorie_tracker_bp
from .shopping_list import shopping_list_bp
from .notifications import notifications_bp

__all__ = [
    'main_bp',
    'auth_bp', 
    'profile_bp',
    'recipes_bp',
    'api_bp',
    'calendar_bp',
    'calorie_tracker_bp',
    'shopping_list_bp',
    'notifications_bp'
]
