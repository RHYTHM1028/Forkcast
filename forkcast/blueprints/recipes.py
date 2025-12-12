"""
Recipes Blueprint - Recipe viewing and management pages.

This blueprint handles:
    - Public recipe feed
    - User's personal recipes page
"""

from flask import Blueprint, render_template, session

from ..models import get_db_cursor
from ..helpers import login_required, get_current_user

# Create the blueprint
recipes_bp = Blueprint(
    'recipes',
    __name__,
    template_folder='../templates'
)


@recipes_bp.route('/recipes')
@login_required
def recipes():
    """
    Public recipe feed page.
    Shows all public recipes from all users.
    """
    with get_db_cursor() as cur:
        cur.execute('''
            SELECT r.*, r.calories_per_serving as calories, u.username, u.full_name, u.profile_image,
                   COALESCE(AVG(rr.rating), 0) as avg_rating,
                   COUNT(DISTINCT rr.id) as rating_count
            FROM recipes r
            JOIN users u ON r.user_id = u.id
            LEFT JOIN recipe_ratings rr ON r.id = rr.recipe_id
            WHERE r.is_public = true
            GROUP BY r.id, u.username, u.full_name, u.profile_image
            ORDER BY r.created_at DESC
        ''')
        all_recipes = cur.fetchall()
    
    user = get_current_user()
    return render_template('recipe.html', user=user, recipes=all_recipes)


@recipes_bp.route('/my-recipes')
@login_required
def my_recipes():
    """
    User's personal recipes page.
    Shows recipes created by the logged-in user.
    """
    with get_db_cursor() as cur:
        cur.execute('''
            SELECT r.*, r.calories_per_serving as calories,
                   COALESCE(AVG(rr.rating), 0) as avg_rating,
                   COUNT(DISTINCT rr.id) as rating_count
            FROM recipes r
            LEFT JOIN recipe_ratings rr ON r.id = rr.recipe_id
            WHERE r.user_id = %s
            GROUP BY r.id
            ORDER BY r.created_at DESC
        ''', (session['user_id'],))
        user_recipes = cur.fetchall()
    
    user = get_current_user()
    return render_template('my_recipes.html', user=user, recipes=user_recipes)
