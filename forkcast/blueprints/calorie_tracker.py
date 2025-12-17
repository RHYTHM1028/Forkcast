"""
Calorie Tracker Blueprint - Calorie tracking features.

This blueprint handles:
    - Calorie tracker page view
    - Today's meals from calendar/meal plans
    - Serving size adjustment and nutrition calculation
"""

from flask import Blueprint, render_template, request, jsonify, session
from datetime import datetime, date, timedelta
from psycopg2.extras import Json

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
    
    # Get date from query parameter or use today
    date_str = request.args.get('date')
    if date_str:
        try:
            today = date.fromisoformat(date_str)
        except ValueError:
            today = date.today()
    else:
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
                    # The calendar stores meals as arrays: [{"recipeId": 1, "recipeName": "...", "servings": 1.5}]
                    if isinstance(meal_info, list):
                        # It's an array - process each meal in the slot
                        for single_meal in meal_info:
                            recipe_id = single_meal.get('recipeId') if isinstance(single_meal, dict) else None
                            saved_servings = single_meal.get('servings', 1) if isinstance(single_meal, dict) else 1
                            print(f"DEBUG: Recipe ID from array: {recipe_id}")
                            print(f"DEBUG: Saved servings: {saved_servings}")
                            
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
                                        'current_servings': saved_servings,
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
                        saved_servings = meal_info.get('servings', 1)
                        print(f"DEBUG: Recipe ID from object: {recipe_id}")
                        print(f"DEBUG: Saved servings: {saved_servings}")
                        
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
                                    'current_servings': saved_servings,
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
    """Get user's calorie and nutrition goals."""
    user_id = session['user_id']
    target_date = request.args.get('date', date.today().isoformat())
    
    with get_db_cursor() as cur:
        # Check if user_nutrition_goals table exists, if not create it
        cur.execute('''
            CREATE TABLE IF NOT EXISTS user_nutrition_goals (
                user_id INTEGER PRIMARY KEY REFERENCES users(id) ON DELETE CASCADE,
                calorie_goal INTEGER DEFAULT 2000,
                protein_goal INTEGER DEFAULT 150,
                carbs_goal INTEGER DEFAULT 200,
                fats_goal INTEGER DEFAULT 67,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Get user's goals
        cur.execute('''
            SELECT calorie_goal, protein_goal, carbs_goal, fats_goal
            FROM user_nutrition_goals
            WHERE user_id = %s
        ''', (user_id,))
        result = cur.fetchone()
        
        if result:
            return jsonify({
                'success': True,
                'date': target_date,
                'calorie_goal': result['calorie_goal'] or 2000,
                'protein_goal': result['protein_goal'] or 150,
                'carbs_goal': result['carbs_goal'] or 200,
                'fats_goal': result['fats_goal'] or 67
            })
        else:
            # Return defaults if no goals set
            return jsonify({
                'success': True,
                'date': target_date,
                'calorie_goal': 2000,
                'protein_goal': 150,
                'carbs_goal': 200,
                'fats_goal': 67
            })


@calorie_tracker_bp.route('/api/daily-summary', methods=['POST'])
@login_required
def save_daily_summary():
    """Save user's nutrition goals and preferences."""
    user_id = session['user_id']
    data = request.get_json()
    
    calorie_goal = data.get('calorie_goal', 2000)
    protein_goal = data.get('protein_goal', 150)
    carbs_goal = data.get('carbs_goal', 200)
    fats_goal = data.get('fats_goal', 67)
    
    with get_db_cursor(commit=True) as cur:
        # Insert or update user's nutrition goals
        cur.execute('''
            INSERT INTO user_nutrition_goals (user_id, calorie_goal, protein_goal, carbs_goal, fats_goal, updated_at)
            VALUES (%s, %s, %s, %s, %s, CURRENT_TIMESTAMP)
            ON CONFLICT (user_id) 
            DO UPDATE SET 
                calorie_goal = EXCLUDED.calorie_goal,
                protein_goal = EXCLUDED.protein_goal,
                carbs_goal = EXCLUDED.carbs_goal,
                fats_goal = EXCLUDED.fats_goal,
                updated_at = CURRENT_TIMESTAMP
        ''', (user_id, calorie_goal, protein_goal, carbs_goal, fats_goal))
    
    return jsonify({
        'success': True,
        'message': 'Nutrition goals updated successfully',
        'calorie_goal': calorie_goal,
        'protein_goal': protein_goal,
        'carbs_goal': carbs_goal,
        'fats_goal': fats_goal
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


@calorie_tracker_bp.route('/api/save-serving', methods=['POST'])
@login_required
def save_serving_size():
    """Save serving size for a specific meal on a specific date."""
    user_id = session['user_id']
    data = request.get_json()
    
    recipe_id = data.get('recipe_id')
    meal_type = data.get('meal_type', '').lower()
    servings = float(data.get('servings', 1))
    date_str = data.get('date')
    
    if not recipe_id or not meal_type or not date_str:
        return jsonify({'success': False, 'error': 'Missing required fields'}), 400
    
    try:
        target_date = date.fromisoformat(date_str)
    except ValueError:
        return jsonify({'success': False, 'error': 'Invalid date format'}), 400
    
    # Calculate week start for the target date
    days_since_sunday = (target_date.weekday() + 1) % 7
    week_start = target_date - timedelta(days=days_since_sunday)
    day_index = (target_date.weekday() + 1) % 7
    
    with get_db_cursor(commit=True) as cur:
        # Get current calendar data for this week
        cur.execute('''
            SELECT meals FROM weekly_calendar_data 
            WHERE user_id = %s AND week_start_date = %s
        ''', (user_id, week_start))
        result = cur.fetchone()
        
        if not result:
            return jsonify({'success': False, 'error': 'No calendar data found for this week'}), 404
        
        meals = result['meals'] or {}
        slot_key = f"{day_index}-{meal_type}"
        
        # Update servings for the specific recipe in this slot
        if slot_key in meals:
            meal_info = meals[slot_key]
            
            if isinstance(meal_info, list):
                # Find and update the specific recipe in the array
                for meal in meal_info:
                    if meal.get('recipeId') == recipe_id:
                        meal['servings'] = servings
                        break
            else:
                # Old format - single object
                if meal_info.get('recipeId') == recipe_id:
                    meal_info['servings'] = servings
            
            # Update the database with properly serialized JSON
            cur.execute('''
                UPDATE weekly_calendar_data 
                SET meals = %s
                WHERE user_id = %s AND week_start_date = %s
            ''', (Json(meals), user_id, week_start))
            
            return jsonify({
                'success': True,
                'message': 'Serving size saved',
                'servings': servings
            })
        else:
            return jsonify({'success': False, 'error': 'Meal slot not found'}), 404


@calorie_tracker_bp.route('/api/weekly-average', methods=['GET'])
@login_required
def get_weekly_average():
    """Get weekly average calories and macros for the week containing the specified date."""
    user_id = session['user_id']
    
    # Get date from query parameter or use today
    date_str = request.args.get('date')
    if date_str:
        try:
            target_date = date.fromisoformat(date_str)
        except ValueError:
            target_date = date.today()
    else:
        target_date = date.today()
    
    # Calculate week start (Sunday) and end (Saturday)
    days_since_sunday = (target_date.weekday() + 1) % 7
    week_start = target_date - timedelta(days=days_since_sunday)
    week_end = week_start + timedelta(days=6)
    
    # Format week range
    week_range = f"{week_start.strftime('%b %d')} - {week_end.strftime('%b %d, %Y')}"
    
    with get_db_cursor() as cur:
        # Get all weeks to find the one containing our target date
        cur.execute('''
            SELECT week_start_date, meals FROM weekly_calendar_data 
            WHERE user_id = %s
            ORDER BY week_start_date DESC
            LIMIT 10
        ''', (user_id,))
        all_weeks = cur.fetchall()
        
        # Collect all meals for the 7 days in the week
        daily_totals = []
        
        for day_offset in range(7):
            current_date = week_start + timedelta(days=day_offset)
            day_calories = 0
            day_protein = 0
            day_carbs = 0
            day_fats = 0
            
            # Find the week record containing this date
            for week in all_weeks:
                db_week_start = week['week_start_date']
                db_week_end = db_week_start + timedelta(days=6)
                
                if db_week_start <= current_date <= db_week_end:
                    meals = week['meals']
                    if meals:
                        # Calculate day index
                        day_index = (current_date.weekday() + 1) % 7
                        meal_types = ['breakfast', 'lunch', 'dinner', 'snack']
                        
                        for meal_type in meal_types:
                            slot_key = f"{day_index}-{meal_type}"
                            if slot_key in meals and meals[slot_key]:
                                meal_info = meals[slot_key]
                                
                                if isinstance(meal_info, list):
                                    for single_meal in meal_info:
                                        recipe_id = single_meal.get('recipeId')
                                        if recipe_id:
                                            cur.execute('''
                                                SELECT calories_per_serving 
                                                FROM recipes 
                                                WHERE id = %s
                                            ''', (recipe_id,))
                                            recipe = cur.fetchone()
                                            
                                            if recipe:
                                                calories = recipe['calories_per_serving'] or 0
                                                day_calories += calories
                                                day_protein += int((calories * 0.30) / 4)
                                                day_carbs += int((calories * 0.40) / 4)
                                                day_fats += int((calories * 0.30) / 9)
                    break
            
            # Only count days that have data
            if day_calories > 0:
                daily_totals.append({
                    'calories': day_calories,
                    'protein': day_protein,
                    'carbs': day_carbs,
                    'fats': day_fats
                })
        
        # Calculate averages
        if daily_totals:
            avg_calories = sum(d['calories'] for d in daily_totals) / len(daily_totals)
            avg_protein = sum(d['protein'] for d in daily_totals) / len(daily_totals)
            avg_carbs = sum(d['carbs'] for d in daily_totals) / len(daily_totals)
            avg_fats = sum(d['fats'] for d in daily_totals) / len(daily_totals)
        else:
            avg_calories = avg_protein = avg_carbs = avg_fats = 0
        
        return jsonify({
            'success': True,
            'week_range': week_range,
            'avg_calories': avg_calories,
            'avg_protein': avg_protein,
            'avg_carbs': avg_carbs,
            'avg_fats': avg_fats,
            'days_with_data': len(daily_totals)
        })
