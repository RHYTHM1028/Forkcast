"""
Calorie Tracker Blueprint - Calorie tracking features.

This blueprint handles:
    - Calorie tracker page view
    - Today's meals from calendar/meal plans
    - Serving size adjustment and nutrition calculation
"""

from flask import Blueprint, render_template, request, jsonify, session
from datetime import datetime, date, timedelta

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


@calorie_tracker_bp.route('/api/todays-meals', methods=['GET'])
@login_required
def get_todays_meals():
    """Get today's meals from the calendar/meal plans with recipe details."""
    user_id = session['user_id']
    today = date.today()
    
    # Get the week start date for today (Sunday as week start)
    # Python weekday(): 0=Monday, 6=Sunday
    # We want: 0=Sunday, 6=Saturday
    # So we convert: (weekday + 1) % 7 gives us Sunday=0
    days_since_sunday = (today.weekday() + 1) % 7  # 0 = Sunday, 6 = Saturday
    week_start = today - timedelta(days=days_since_sunday)
    
    meals_data = []
    
    with get_db_cursor() as cur:
        # Debug: First check what weeks exist for this user
        cur.execute('''
            SELECT week_start_date, meals FROM weekly_calendar_data 
            WHERE user_id = %s
            ORDER BY week_start_date DESC
            LIMIT 5
        ''', (user_id,))
        all_weeks = cur.fetchall()
        
        print(f"DEBUG: Today's date: {today}")
        print(f"DEBUG: Calculated week_start: {week_start}")
        print(f"DEBUG: User ID: {user_id}")
        print(f"DEBUG: All weeks in DB: {[(str(w['week_start_date']), w['meals']) for w in all_weeks] if all_weeks else 'None'}")
        
        # Try to find the week that contains today
        result = None
        matched_week_start = None
        
        for week in all_weeks:
            db_week_start = week['week_start_date']
            # Check if today falls within this week (week_start to week_start + 6 days)
            if db_week_start <= today <= db_week_start + timedelta(days=6):
                result = week
                matched_week_start = db_week_start
                print(f"DEBUG: Matched week_start from DB: {db_week_start}")
                break
        
        # Debug logging
        print(f"DEBUG: Database result: {result}")
        
        if result and result['meals']:
            meals = result['meals']
            print(f"DEBUG: Meals data: {meals}")
            
            # Parse today's meals from the JSONB structure
            # The meals structure uses dayIndex (0=Sunday, 1=Monday, etc.): {"0-breakfast": [...], ...}
            # Convert Python weekday (Mon=0, Sun=6) to our format (Sun=0, Sat=6)
            day_index = (today.weekday() + 1) % 7  # 0 = Sunday, 6 = Saturday
            print(f"DEBUG: Day index (Sunday=0): {day_index}")
            print(f"DEBUG: All keys in meals: {list(meals.keys())}")
            meal_types = ['breakfast', 'lunch', 'dinner', 'snack']
            
            for meal_type in meal_types:
                slot_key = f"{day_index}-{meal_type}"
                print(f"DEBUG: Checking slot_key: {slot_key}")
                if slot_key in meals and meals[slot_key]:
                    meal_info = meals[slot_key]
                    print(f"DEBUG: Found meal_info (type={type(meal_info).__name__}): {meal_info}")
                    
                    # Handle both array format and object format
                    # The calendar stores meals as arrays: [{"recipeId": 1, "recipeName": "..."}]
                    if isinstance(meal_info, list):
                        # It's an array - process each meal in the slot
                        for single_meal in meal_info:
                            recipe_id = single_meal.get('recipeId') if isinstance(single_meal, dict) else None
                            print(f"DEBUG: Recipe ID from array: {recipe_id}")
                            
                            if recipe_id:
                                # Get full recipe details including nutrition
                                cur.execute('''
                                    SELECT id, title, description, ingredients, servings, 
                                           calories_per_serving, prep_time, cook_time, image_url
                                    FROM recipes 
                                    WHERE id = %s
                                ''', (recipe_id,))
                                recipe = cur.fetchone()
                                
                                if recipe:
                                    print(f"DEBUG: Found recipe: {recipe['title']}")
                                    meals_data.append({
                                        'recipe_id': recipe['id'],
                                        'title': recipe['title'],
                                        'description': recipe['description'],
                                        'ingredients': recipe['ingredients'],
                                        'meal_type': meal_type.upper(),
                                        'base_servings': recipe['servings'] or 1,
                                        'current_servings': 1,
                                        'calories_per_serving': recipe['calories_per_serving'] or 0,
                                        'prep_time': recipe['prep_time'],
                                        'cook_time': recipe['cook_time'],
                                        'image_url': recipe['image_url']
                                    })
                                else:
                                    print(f"DEBUG: Recipe not found for ID: {recipe_id}")
                    else:
                        # It's a single object (old format)
                        recipe_id = meal_info.get('recipeId')
                        print(f"DEBUG: Recipe ID from object: {recipe_id}")
                        
                        if recipe_id:
                            # Get full recipe details including nutrition
                            cur.execute('''
                                SELECT id, title, description, ingredients, servings, 
                                       calories_per_serving, prep_time, cook_time, image_url
                                FROM recipes 
                                WHERE id = %s
                            ''', (recipe_id,))
                            recipe = cur.fetchone()
                            
                            if recipe:
                                print(f"DEBUG: Found recipe: {recipe['title']}")
                                meals_data.append({
                                    'recipe_id': recipe['id'],
                                    'title': recipe['title'],
                                    'description': recipe['description'],
                                    'ingredients': recipe['ingredients'],
                                    'meal_type': meal_type.upper(),
                                    'base_servings': recipe['servings'] or 1,
                                    'current_servings': 1,
                                    'calories_per_serving': recipe['calories_per_serving'] or 0,
                                    'prep_time': recipe['prep_time'],
                                    'cook_time': recipe['cook_time'],
                                    'image_url': recipe['image_url']
                                })
                            else:
                                print(f"DEBUG: Recipe not found for ID: {recipe_id}")
    
    print(f"DEBUG: Total meals found: {len(meals_data)}")
    print(f"DEBUG: Returning meals_data: {meals_data}")
    return jsonify({'success': True, 'meals': meals_data})


@calorie_tracker_bp.route('/api/debug-calendar', methods=['GET'])
@login_required
def debug_calendar():
    """Debug endpoint to see what's in the calendar database."""
    user_id = session['user_id']
    today = date.today()
    
    with get_db_cursor() as cur:
        # Get all calendar data for this user
        cur.execute('''
            SELECT week_start_date, meals 
            FROM weekly_calendar_data 
            WHERE user_id = %s
            ORDER BY week_start_date DESC
            LIMIT 5
        ''', (user_id,))
        all_weeks = cur.fetchall()
        
        return jsonify({
            'success': True,
            'user_id': user_id,
            'today': today.isoformat(),
            'today_weekday': today.weekday(),
            'today_day_index': (today.weekday() + 1) % 7,  # Sunday=0 format
            'all_calendar_weeks': [
                {
                    'week_start': str(week['week_start_date']),
                    'meals': week['meals']
                } for week in all_weeks
            ] if all_weeks else []
        })


@calorie_tracker_bp.route('/api/recipe/<int:recipe_id>/nutrition', methods=['GET'])
@login_required
def get_recipe_nutrition(recipe_id):
    """Get detailed nutrition info for a recipe."""
    servings = float(request.args.get('servings', 1))
    
    with get_db_cursor() as cur:
        cur.execute('''
            SELECT id, title, ingredients, servings, calories_per_serving 
            FROM recipes 
            WHERE id = %s
        ''', (recipe_id,))
        recipe = cur.fetchone()
        
        if not recipe:
            return jsonify({'success': False, 'error': 'Recipe not found'}), 404
        
        # Calculate nutrition based on serving size
        base_servings = recipe['servings'] or 1
        calories_per_serving = recipe['calories_per_serving'] or 0
        
        # Total calories for requested servings
        total_calories = int(calories_per_serving * servings)
        
        # Estimate macros (rough estimation based on calories)
        # Using general ratios: 40% carbs, 30% protein, 30% fat
        protein_grams = int((total_calories * 0.30) / 4)  # 4 cal per gram
        carbs_grams = int((total_calories * 0.40) / 4)    # 4 cal per gram
        fats_grams = int((total_calories * 0.30) / 9)     # 9 cal per gram
        
        return jsonify({
            'success': True,
            'recipe_id': recipe['id'],
            'title': recipe['title'],
            'servings': servings,
            'base_servings': base_servings,
            'calories': total_calories,
            'protein': protein_grams,
            'carbs': carbs_grams,
            'fats': fats_grams,
            'ingredients': recipe['ingredients']
        })


@calorie_tracker_bp.route('/api/daily-summary', methods=['GET'])
@login_required
def get_daily_summary():
    """Get today's calorie and nutrition summary."""
    user_id = session['user_id']
    target_date = request.args.get('date', date.today().isoformat())
    
    # This endpoint can be extended to store and retrieve daily summaries
    # For now, it returns default targets
    return jsonify({
        'success': True,
        'date': target_date,
        'calorie_goal': 2000,
        'protein_goal': 120,
        'carbs_goal': 250,
        'fats_goal': 65
    })


@calorie_tracker_bp.route('/api/daily-summary', methods=['POST'])
@login_required
def save_daily_summary():
    """Save daily calorie goal and preferences."""
    user_id = session['user_id']
    data = request.get_json()
    
    calorie_goal = data.get('calorie_goal', 2000)
    
    # This could be stored in a user preferences table
    # For now, just acknowledge the request
    return jsonify({
        'success': True,
        'message': 'Daily goals updated',
        'calorie_goal': calorie_goal
    })


@calorie_tracker_bp.route('/api/logs', methods=['GET'])
@login_required
def get_calorie_logs():
    """Get calorie logs for the logged-in user."""
    user_id = session['user_id']
    date = request.args.get('date')
    
    query = '''
        SELECT cl.*, r.title as recipe_name, r.calories_per_serving as recipe_calories
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
