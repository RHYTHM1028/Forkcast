"""
API Blueprint - RESTful API endpoints for AJAX operations.

This blueprint handles all API endpoints for:
    - Recipe CRUD operations
    - Recipe ratings and reviews
    - Other AJAX-based operations

All routes are prefixed with /api when registered.
"""

from flask import Blueprint, request, redirect, url_for, flash, session, jsonify, current_app
from werkzeug.utils import secure_filename
from datetime import datetime
import os

from ..models import get_db_cursor
from ..helpers import login_required, allowed_file
from ..ingredient_parser import parse_ingredient, estimate_grams, extract_food_name
from .notifications import create_review_notification

# Create the blueprint
api_bp = Blueprint(
    'api',
    __name__,
    url_prefix='/api'
)


# ==================== RECIPE ENDPOINTS ====================

@api_bp.route('/recipes', methods=['GET'])
@login_required
def get_recipes():
    """
    Get recipes list.
    
    Query params:
        type: 'my' for user's recipes, 'all' for public recipes (default)
    """
    recipe_type = request.args.get('type', 'all')
    
    with get_db_cursor() as cur:
        if recipe_type == 'my':
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
        else:
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
        recipes = cur.fetchall()
    
    return jsonify({'success': True, 'recipes': recipes})


@api_bp.route('/recipes/<int:recipe_id>', methods=['GET'])
@login_required
def get_recipe(recipe_id):
    """Get single recipe by ID."""
    with get_db_cursor() as cur:
        cur.execute('''
            SELECT r.*, r.calories_per_serving as calories, u.username, u.full_name, u.profile_image,
                   r.forked_from_id, r.original_author_id,
                   COALESCE(AVG(rr.rating), 0) as avg_rating,
                   COUNT(DISTINCT rr.id) as rating_count,
                   orig.title as original_title,
                   orig.is_public as original_is_public,
                   orig_user.username as original_author_username,
                   orig_user.full_name as original_author_name
            FROM recipes r
            JOIN users u ON r.user_id = u.id
            LEFT JOIN recipe_ratings rr ON r.id = rr.recipe_id
            LEFT JOIN recipes orig ON r.forked_from_id = orig.id
            LEFT JOIN users orig_user ON r.original_author_id = orig_user.id
            WHERE r.id = %s
            GROUP BY r.id, u.username, u.full_name, u.profile_image, 
                     orig.title, orig.is_public, orig_user.username, orig_user.full_name
        ''', (recipe_id,))
        recipe_row = cur.fetchone()
        
        if not recipe_row:
            return jsonify({'success': False, 'message': 'Recipe not found'}), 404
        
        # Convert to regular dict and handle Decimal/datetime types
        recipe = {}
        for key, value in recipe_row.items():
            if hasattr(value, 'isoformat'):  # datetime objects
                recipe[key] = value.isoformat()
            elif isinstance(value, (int, float, str, bool, type(None))):
                recipe[key] = value
            else:
                recipe[key] = float(value) if hasattr(value, '__float__') else str(value)
        
        # Ensure proper types
        if recipe.get('avg_rating') is not None:
            recipe['avg_rating'] = float(recipe['avg_rating'])
        if recipe.get('rating_count') is not None:
            recipe['rating_count'] = int(recipe['rating_count'])
        
        cur.execute('SELECT rating, review FROM recipe_ratings WHERE recipe_id = %s AND user_id = %s', 
                    (recipe_id, session['user_id']))
        user_rating_row = cur.fetchone()
        user_rating = dict(user_rating_row) if user_rating_row else None
    
    return jsonify({
        'success': True, 
        'recipe': recipe,
        'user_rating': user_rating
    })


@api_bp.route('/recipes', methods=['POST'])
@login_required
def create_recipe():
    """Create a new recipe."""
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest' or request.is_json
    
    title = request.form.get('title', '').strip()
    description = request.form.get('description', '').strip()
    ingredients = request.form.get('ingredients', '').strip()
    instructions = request.form.get('instructions', '').strip()
    prep_time = request.form.get('prep_time')
    cook_time = request.form.get('cook_time')
    servings = request.form.get('servings')
    calories = request.form.get('calories_per_serving')
    category = request.form.get('category', '').strip()
    cuisine = request.form.get('cuisine', '').strip()
    difficulty = request.form.get('difficulty', '').strip()
    tags = request.form.get('tags', '').strip()
    is_public = request.form.get('is_public', 'true') == 'true'
    
    if not title or not ingredients or not instructions:
        message = 'Title, ingredients, and instructions are required.'
        if is_ajax:
            return jsonify({'success': False, 'message': message})
        flash(message, 'error')
        return redirect(url_for('recipes.my_recipes'))
    
    
    # Handle image upload
    image_url = None
    if 'recipe_image' in request.files:
        file = request.files['recipe_image']
        if file and file.filename and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            unique_filename = f"{session['user_id']}_{timestamp}_{filename}"
            file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], 'recipes', unique_filename)
            file.save(file_path)
            image_url = f"/static/uploads/recipes/{unique_filename}"
    
    try:
        with get_db_cursor(commit=True) as cur:
            cur.execute('''
                INSERT INTO recipes (user_id, title, description, ingredients, instructions,
                                   prep_time, cook_time, servings, calories_per_serving,
                                   category, cuisine, difficulty, tags, is_public, image_url)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING id
            ''', (session['user_id'], title, description, ingredients, instructions,
                  prep_time, cook_time, servings, calories, category, cuisine, difficulty, 
                  tags, is_public, image_url))
            recipe_id = cur.fetchone()['id']
        
        if is_ajax:
            return jsonify({'success': True, 'message': 'Recipe created successfully!', 'recipe_id': recipe_id})
        
        flash('Recipe created successfully!', 'success')
        return redirect(url_for('recipes.my_recipes'))
        
    except Exception as e:
        message = 'An error occurred. Please try again.'
        print(f"Error: {e}")
        if is_ajax:
            return jsonify({'success': False, 'message': message})
        flash(message, 'error')
    
    return redirect(url_for('recipes.my_recipes'))


@api_bp.route('/recipes/<int:recipe_id>', methods=['PUT', 'POST'])
@login_required
def update_recipe(recipe_id):
    """Update an existing recipe."""
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest' or request.is_json
    
    with get_db_cursor() as cur:
        cur.execute('SELECT user_id, image_url FROM recipes WHERE id = %s', (recipe_id,))
        recipe = cur.fetchone()
    
    if not recipe or recipe['user_id'] != session['user_id']:
        message = 'Recipe not found or you do not have permission to edit it.'
        if is_ajax:
            return jsonify({'success': False, 'message': message}), 403
        flash(message, 'error')
        return redirect(url_for('recipes.my_recipes'))
    
    title = request.form.get('title', '').strip()
    description = request.form.get('description', '').strip()
    ingredients = request.form.get('ingredients', '').strip()
    instructions = request.form.get('instructions', '').strip()
    prep_time = request.form.get('prep_time')
    cook_time = request.form.get('cook_time')
    servings = request.form.get('servings')
    calories = request.form.get('calories_per_serving')
    category = request.form.get('category', '').strip()
    cuisine = request.form.get('cuisine', '').strip()
    difficulty = request.form.get('difficulty', '').strip()
    tags = request.form.get('tags', '').strip()
    is_public = request.form.get('is_public', 'true') == 'true'
    
    # Handle image upload
    image_url = recipe.get('image_url')
    if 'recipe_image' in request.files:
        file = request.files['recipe_image']
        if file and file.filename and allowed_file(file.filename):
            # Delete old image if exists
            if image_url:
                old_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), image_url.lstrip('/'))
                if os.path.exists(old_path):
                    os.remove(old_path)
            
            filename = secure_filename(file.filename)
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            unique_filename = f"{session['user_id']}_{timestamp}_{filename}"
            file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], 'recipes', unique_filename)
            file.save(file_path)
            image_url = f"/static/uploads/recipes/{unique_filename}"
    
    try:
        with get_db_cursor(commit=True) as cur:
            cur.execute('''
                UPDATE recipes 
                SET title = %s, description = %s, ingredients = %s, instructions = %s,
                    prep_time = %s, cook_time = %s, servings = %s, calories_per_serving = %s,
                    category = %s, cuisine = %s, difficulty = %s, tags = %s, is_public = %s,
                    image_url = %s, updated_at = CURRENT_TIMESTAMP
                WHERE id = %s
            ''', (title, description, ingredients, instructions, prep_time, cook_time,
                  servings, calories, category, cuisine, difficulty, tags, is_public, image_url, recipe_id))
        
        if is_ajax:
            return jsonify({'success': True, 'message': 'Recipe updated successfully!'})
        
        flash('Recipe updated successfully!', 'success')
        return redirect(url_for('recipes.my_recipes'))
        
    except Exception as e:
        message = 'An error occurred. Please try again.'
        print(f"Error: {e}")
        if is_ajax:
            return jsonify({'success': False, 'message': message})
        flash(message, 'error')
    
    return redirect(url_for('recipes.my_recipes'))


@api_bp.route('/recipes/<int:recipe_id>', methods=['DELETE'])
@login_required
def delete_recipe(recipe_id):
    """Delete a recipe."""
    with get_db_cursor() as cur:
        cur.execute('SELECT user_id, title, image_url FROM recipes WHERE id = %s', (recipe_id,))
        recipe = cur.fetchone()
    
    if not recipe or recipe['user_id'] != session['user_id']:
        return jsonify({'success': False, 'message': 'Recipe not found or you do not have permission to delete it.'}), 403
    
    try:
        if recipe.get('image_url'):
            image_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), recipe['image_url'].lstrip('/'))
            if os.path.exists(image_path):
                os.remove(image_path)
        
        with get_db_cursor(commit=True) as cur:
            cur.execute('DELETE FROM recipes WHERE id = %s', (recipe_id,))
        
        return jsonify({'success': True, 'message': f'Recipe "{recipe["title"]}" deleted successfully!'})
        
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'success': False, 'message': 'An error occurred. Please try again.'}), 500


# ==================== FORK RECIPE ENDPOINT ====================

@api_bp.route('/recipes/<int:recipe_id>/fork', methods=['POST'])
@login_required
def fork_recipe(recipe_id):
    """Fork (copy) a public recipe to user's private collection."""
    with get_db_cursor() as cur:
        # Get the original recipe
        cur.execute('''
            SELECT r.*, u.id as author_id, u.username as author_username, u.full_name as author_name
            FROM recipes r
            JOIN users u ON r.user_id = u.id
            WHERE r.id = %s AND (r.is_public = true OR r.user_id = %s)
        ''', (recipe_id, session['user_id']))
        original = cur.fetchone()
    
    if not original:
        return jsonify({'success': False, 'message': 'Recipe not found or not accessible'}), 404
    
    # Don't allow forking own recipe
    if original['user_id'] == session['user_id']:
        return jsonify({'success': False, 'message': 'You cannot fork your own recipe'}), 400
    
    # Check if user already forked this recipe
    with get_db_cursor() as cur:
        cur.execute('''
            SELECT id FROM recipes 
            WHERE user_id = %s AND forked_from_id = %s
        ''', (session['user_id'], recipe_id))
        existing_fork = cur.fetchone()
    
    if existing_fork:
        return jsonify({
            'success': False, 
            'message': 'You have already forked this recipe',
            'forked_recipe_id': existing_fork['id']
        }), 400
    
    try:
        with get_db_cursor(commit=True) as cur:
            # Create the forked recipe (private by default)
            cur.execute('''
                INSERT INTO recipes (
                    user_id, title, description, ingredients, instructions,
                    prep_time, cook_time, servings, calories_per_serving,
                    category, cuisine, difficulty, tags, image_url,
                    is_public, forked_from_id, original_author_id
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING id
            ''', (
                session['user_id'],
                original['title'],
                original['description'],
                original['ingredients'],
                original['instructions'],
                original['prep_time'],
                original['cook_time'],
                original['servings'],
                original['calories_per_serving'],
                original['category'],
                original['cuisine'],
                original['difficulty'],
                original['tags'],
                original['image_url'],
                False,  # is_public = False (private by default)
                recipe_id,  # forked_from_id
                original['user_id']  # original_author_id
            ))
            new_recipe_id = cur.fetchone()['id']
        
        author_name = original['author_name'] or original['author_username']
        return jsonify({
            'success': True,
            'message': f'Recipe forked successfully! It\'s now in your private recipes.',
            'forked_recipe_id': new_recipe_id,
            'original_author': author_name
        })
        
    except Exception as e:
        print(f"Error forking recipe: {e}")
        return jsonify({'success': False, 'message': 'An error occurred. Please try again.'}), 500


# ==================== RATING ENDPOINTS ====================

@api_bp.route('/recipes/<int:recipe_id>/rate', methods=['POST'])
@login_required
def rate_recipe(recipe_id):
    """Rate a recipe."""
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest' or request.is_json
    
    rating = request.form.get('rating')
    review = request.form.get('review', '').strip()
    
    if not rating or not rating.isdigit() or int(rating) < 1 or int(rating) > 5:
        message = 'Rating must be between 1 and 5.'
        if is_ajax:
            return jsonify({'success': False, 'message': message})
        flash(message, 'error')
        return redirect(url_for('recipes.recipes'))
    
    rating = int(rating)
    
    with get_db_cursor() as cur:
        cur.execute('SELECT user_id FROM recipes WHERE id = %s', (recipe_id,))
        recipe = cur.fetchone()
    
    if not recipe:
        message = 'Recipe not found.'
        if is_ajax:
            return jsonify({'success': False, 'message': message}), 404
        flash(message, 'error')
        return redirect(url_for('recipes.recipes'))
    
    recipe_owner_id = recipe['user_id']
    
    if recipe_owner_id == session['user_id']:
        message = 'You cannot rate your own recipe.'
        if is_ajax:
            return jsonify({'success': False, 'message': message})
        flash(message, 'error')
        return redirect(url_for('recipes.recipes'))
    
    try:
        with get_db_cursor(commit=True) as cur:
            cur.execute('''
                INSERT INTO recipe_ratings (recipe_id, user_id, rating, review)
                VALUES (%s, %s, %s, %s)
                ON CONFLICT (recipe_id, user_id) 
                DO UPDATE SET rating = EXCLUDED.rating, 
                             review = EXCLUDED.review,
                             updated_at = CURRENT_TIMESTAMP
            ''', (recipe_id, session['user_id'], rating, review))
        
        # Get recipe title for notification
        with get_db_cursor() as cur:
            cur.execute('SELECT title FROM recipes WHERE id = %s', (recipe_id,))
            recipe_data = cur.fetchone()
            recipe_title = recipe_data['title'] if recipe_data else 'your recipe'
        
        # Create notification for recipe owner
        try:
            create_review_notification(
                recipe_owner_id=recipe_owner_id,
                reviewer_id=session['user_id'],
                recipe_id=recipe_id,
                recipe_title=recipe_title,
                rating=rating,
                review_text=review
            )
        except Exception as notif_error:
            print(f"Failed to create notification: {notif_error}")
        
        with get_db_cursor() as cur:
            cur.execute('''
                SELECT COALESCE(AVG(rating), 0) as avg_rating,
                       COUNT(*) as rating_count
                FROM recipe_ratings
                WHERE recipe_id = %s
            ''', (recipe_id,))
            result = cur.fetchone()
        
        if is_ajax:
            return jsonify({
                'success': True, 
                'message': 'Rating submitted successfully!',
                'avg_rating': float(result['avg_rating']),
                'rating_count': result['rating_count']
            })
        
        flash('Rating submitted successfully!', 'success')
        return redirect(url_for('recipes.recipes'))
        
    except Exception as e:
        message = 'An error occurred. Please try again.'
        print(f"Error: {e}")
        if is_ajax:
            return jsonify({'success': False, 'message': message})
        flash(message, 'error')
    
    return redirect(url_for('recipes.recipes'))


@api_bp.route('/recipes/<int:recipe_id>/reviews', methods=['GET'])
@login_required
def get_recipe_reviews(recipe_id):
    """Get all reviews for a recipe."""
    with get_db_cursor() as cur:
        cur.execute('''
            SELECT rr.id, rr.rating, rr.review, rr.created_at, rr.updated_at,
                   u.id as user_id, u.username, u.full_name, u.profile_image
            FROM recipe_ratings rr
            JOIN users u ON rr.user_id = u.id
            WHERE rr.recipe_id = %s
            ORDER BY rr.created_at DESC
        ''', (recipe_id,))
        reviews = cur.fetchall()
    
    result = []
    for review in reviews:
        review_dict = dict(review)
        if review_dict.get('created_at'):
            review_dict['created_at'] = review_dict['created_at'].isoformat()
        if review_dict.get('updated_at'):
            review_dict['updated_at'] = review_dict['updated_at'].isoformat()
        result.append(review_dict)
    
    return jsonify({'success': True, 'reviews': result})


@api_bp.route('/my-recipes/reviews', methods=['GET'])
@login_required
def get_my_recipe_reviews():
    """Get all reviews for the current user's recipes."""
    with get_db_cursor() as cur:
        cur.execute('''
            SELECT rr.id, rr.rating, rr.review, rr.created_at, rr.updated_at,
                   rr.recipe_id,
                   r.title as recipe_title, r.image_url as recipe_image,
                   u.id as reviewer_id, u.username as reviewer_username, 
                   u.full_name as reviewer_name, u.profile_image as reviewer_image
            FROM recipe_ratings rr
            JOIN recipes r ON rr.recipe_id = r.id
            JOIN users u ON rr.user_id = u.id
            WHERE r.user_id = %s
            ORDER BY rr.created_at DESC
        ''', (session['user_id'],))
        reviews = cur.fetchall()
    
    result = []
    for review in reviews:
        review_dict = dict(review)
        if review_dict.get('created_at'):
            review_dict['created_at'] = review_dict['created_at'].isoformat()
        if review_dict.get('updated_at'):
            review_dict['updated_at'] = review_dict['updated_at'].isoformat()
        result.append(review_dict)
    
    return jsonify({'success': True, 'reviews': result})


# ==================== RECIPES LIST FOR CALENDAR ====================

@api_bp.route('/recipes/list', methods=['GET'])
@login_required
def get_recipes_for_calendar():
    """Get all recipes for the meal planner (user's own + public recipes)."""
    user_id = session['user_id']
    search = request.args.get('search', '').strip()
    
    query = '''
        SELECT DISTINCT r.id, r.title, r.description, r.prep_time, r.cook_time, 
               r.category, r.calories_per_serving, r.image_url
        FROM recipes r
        WHERE (r.user_id = %s OR r.is_public = true)
    '''
    params = [user_id]
    
    if search:
        query += ' AND (LOWER(r.title) LIKE LOWER(%s) OR LOWER(r.category) LIKE LOWER(%s))'
        search_pattern = f'%{search}%'
        params.extend([search_pattern, search_pattern])
    
    query += ' ORDER BY r.title'
    
    with get_db_cursor() as cur:
        cur.execute(query, params)
        recipes = cur.fetchall()
    
    return jsonify([dict(r) for r in recipes] if recipes else [])


# ==================== INGREDIENT PARSING ENDPOINT ====================

@api_bp.route('/parse-ingredients', methods=['POST'])
@login_required
def parse_ingredients_api():
    """
    Parse ingredient strings and return structured data with gram estimates.
    
    Request body:
        {
            "ingredients": ["2 cups flour", "1/2 tsp salt", ...]
        }
    
    Returns:
        {
            "success": true,
            "parsed": [
                {
                    "original": "2 cups flour",
                    "quantity": 2.0,
                    "unit": "cups",
                    "name": "flour",
                    "foodName": "flour",
                    "gramsEstimate": 480
                },
                ...
            ]
        }
    """
    data = request.get_json()
    ingredients = data.get('ingredients', [])
    
    if not ingredients:
        return jsonify({'success': False, 'message': 'No ingredients provided'})
    
    parsed_results = []
    for ingredient_text in ingredients:
        parsed = parse_ingredient(ingredient_text)
        if parsed:
            result = {
                'original': parsed['original'],
                'quantity': parsed['quantity'],
                'unit': parsed['unit'],
                'name': parsed['name'],
                'foodName': extract_food_name(parsed),
                'gramsEstimate': estimate_grams(parsed)
            }
            parsed_results.append(result)
    
    return jsonify({
        'success': True,
        'parsed': parsed_results
    })
