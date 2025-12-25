"""
Dashboard Blueprint - Personalized user dashboard.

This blueprint handles:
    - Dashboard page rendering
    - Dashboard statistics API
    - Nutrition overview API
    - Recent meals API
    - Upcoming meals API
    - Goals progress API
    - Weekly trend API
"""

from datetime import datetime, date, timedelta
from flask import (
    Blueprint, render_template, request, jsonify, session
)

from ..models import get_db_cursor
from ..helpers import login_required, get_current_user

# Create the blueprint
dashboard_bp = Blueprint(
    'dashboard',
    __name__,
    template_folder='../templates'
)


@dashboard_bp.route('/dashboard')
@login_required
def dashboard():
    """User dashboard page."""
    user = get_current_user()
    return render_template('dashboard.html', user=user)


@dashboard_bp.route('/api/dashboard/stats')
@login_required
def get_dashboard_stats():
    """Get dashboard statistics including calories, meals, recipes, and streak."""
    user_id = session['user_id']
    today = date.today()
    
    with get_db_cursor() as cur:
        # Get today's calorie data from calorie tracker
        days_since_sunday = (today.weekday() + 1) % 7
        week_start = today - timedelta(days=days_since_sunday)
        day_index = (today.weekday() + 1) % 7
        
        # Get user's calorie goal
        cur.execute('''
            SELECT calorie_goal FROM user_nutrition_goals 
            WHERE user_id = %s
        ''', (user_id,))
        goal_result = cur.fetchone()
        calorie_goal = goal_result['calorie_goal'] if goal_result else 2000
        
        # Get today's meals and calculate calories
        cur.execute('''
            SELECT meals FROM weekly_calendar_data 
            WHERE user_id = %s AND week_start_date = %s
        ''', (user_id, week_start))
        calendar_result = cur.fetchone()
        
        today_calories = 0
        if calendar_result and calendar_result['meals']:
            meals = calendar_result['meals']
            meal_types = ['breakfast', 'lunch', 'dinner', 'snack']
            
            for meal_type in meal_types:
                slot_key = f"{day_index}-{meal_type}"
                if slot_key in meals and meals[slot_key]:
                    meal_info = meals[slot_key]
                    meal_list = meal_info if isinstance(meal_info, list) else [meal_info]
                    
                    for single_meal in meal_list:
                        if isinstance(single_meal, dict):
                            recipe_id = single_meal.get('recipeId')
                            servings = single_meal.get('servings', 1)
                            if recipe_id:
                                cur.execute('''
                                    SELECT calories_per_serving 
                                    FROM recipes WHERE id = %s
                                ''', (recipe_id,))
                                recipe = cur.fetchone()
                                if recipe:
                                    today_calories += (recipe['calories_per_serving'] or 0) * servings
        
        # Get weekly meals count
        weekly_meals_count = 0
        week_end = week_start + timedelta(days=6)
        
        if calendar_result and calendar_result['meals']:
            meals = calendar_result['meals']
            for day in range(7):
                for meal_type in ['breakfast', 'lunch', 'dinner', 'snack']:
                    slot_key = f"{day}-{meal_type}"
                    if slot_key in meals and meals[slot_key]:
                        meal_info = meals[slot_key]
                        if isinstance(meal_info, list):
                            weekly_meals_count += len(meal_info)
                        else:
                            weekly_meals_count += 1
        
        # Get saved recipes count
        cur.execute('''
            SELECT COUNT(*) as count FROM recipes 
            WHERE user_id = %s
        ''', (user_id,))
        saved_recipes = cur.fetchone()['count']
        
        return jsonify({
            'success': True,
            'today_calories': int(today_calories),
            'calorie_goal': calorie_goal,
            'weekly_meals': weekly_meals_count,
            'saved_recipes': saved_recipes
        })


@dashboard_bp.route('/api/dashboard/nutrition-overview')
@login_required
def get_nutrition_overview():
    """Get nutrition overview data (protein, carbs, fats)."""
    user_id = session['user_id']
    period = request.args.get('period', 'today')
    today = date.today()
    
    with get_db_cursor() as cur:
        # Get user's nutrition goals
        cur.execute('''
            SELECT protein_goal, carbs_goal, fats_goal 
            FROM user_nutrition_goals 
            WHERE user_id = %s
        ''', (user_id,))
        goals = cur.fetchone()
        
        protein_goal = goals['protein_goal'] if goals else 150
        carbs_goal = goals['carbs_goal'] if goals else 200
        fats_goal = goals['fats_goal'] if goals else 67
        
        # Calculate actual consumption based on period
        if period == 'today':
            days_since_sunday = (today.weekday() + 1) % 7
            week_start = today - timedelta(days=days_since_sunday)
            day_index = (today.weekday() + 1) % 7
            
            cur.execute('''
                SELECT meals FROM weekly_calendar_data 
                WHERE user_id = %s AND week_start_date = %s
            ''', (user_id, week_start))
            result = cur.fetchone()
            
            total_calories = 0
            if result and result['meals']:
                meals = result['meals']
                for meal_type in ['breakfast', 'lunch', 'dinner', 'snack']:
                    slot_key = f"{day_index}-{meal_type}"
                    if slot_key in meals and meals[slot_key]:
                        meal_info = meals[slot_key]
                        meal_list = meal_info if isinstance(meal_info, list) else [meal_info]
                        
                        for single_meal in meal_list:
                            if isinstance(single_meal, dict):
                                recipe_id = single_meal.get('recipeId')
                                servings = single_meal.get('servings', 1)
                                if recipe_id:
                                    cur.execute('''
                                        SELECT calories_per_serving 
                                        FROM recipes WHERE id = %s
                                    ''', (recipe_id,))
                                    recipe = cur.fetchone()
                                    if recipe:
                                        total_calories += (recipe['calories_per_serving'] or 0) * servings
            
            # Estimate macros from calories (rough estimation)
            protein_actual = int((total_calories * 0.30) / 4)
            carbs_actual = int((total_calories * 0.40) / 4)
            fats_actual = int((total_calories * 0.30) / 9)
        
        elif period == 'week':
            # Calculate weekly averages
            days_since_sunday = (today.weekday() + 1) % 7
            week_start = today - timedelta(days=days_since_sunday)
            
            cur.execute('''
                SELECT meals FROM weekly_calendar_data 
                WHERE user_id = %s AND week_start_date = %s
            ''', (user_id, week_start))
            result = cur.fetchone()
            
            total_calories = 0
            days_with_data = 0
            
            if result and result['meals']:
                meals = result['meals']
                for day in range(7):
                    day_calories = 0
                    has_meals = False
                    
                    for meal_type in ['breakfast', 'lunch', 'dinner', 'snack']:
                        slot_key = f"{day}-{meal_type}"
                        if slot_key in meals and meals[slot_key]:
                            meal_info = meals[slot_key]
                            meal_list = meal_info if isinstance(meal_info, list) else [meal_info]
                            
                            for single_meal in meal_list:
                                if isinstance(single_meal, dict):
                                    recipe_id = single_meal.get('recipeId')
                                    servings = single_meal.get('servings', 1)
                                    if recipe_id:
                                        cur.execute('''
                                            SELECT calories_per_serving 
                                            FROM recipes WHERE id = %s
                                        ''', (recipe_id,))
                                        recipe = cur.fetchone()
                                        if recipe:
                                            day_calories += (recipe['calories_per_serving'] or 0) * servings
                                            has_meals = True
                    
                    if has_meals:
                        total_calories += day_calories
                        days_with_data += 1
            
            avg_calories = total_calories / days_with_data if days_with_data > 0 else 0
            protein_actual = int((avg_calories * 0.30) / 4)
            carbs_actual = int((avg_calories * 0.40) / 4)
            fats_actual = int((avg_calories * 0.30) / 9)
        
        else:  # month
            protein_actual = int(protein_goal * 0.75)
            carbs_actual = int(carbs_goal * 0.70)
            fats_actual = int(fats_goal * 0.80)
        
        return jsonify({
            'success': True,
            'protein': {'actual': protein_actual, 'goal': protein_goal},
            'carbs': {'actual': carbs_actual, 'goal': carbs_goal},
            'fats': {'actual': fats_actual, 'goal': fats_goal}
        })


@dashboard_bp.route('/api/dashboard/recent-meals')
@login_required
def get_recent_meals():
    """Get today's meals only."""
    user_id = session['user_id']
    today = date.today()
    recent_meals = []
    
    with get_db_cursor() as cur:
        # Only check today
        days_since_sunday = (today.weekday() + 1) % 7
        week_start = today - timedelta(days=days_since_sunday)
        day_index = (today.weekday() + 1) % 7
        
        cur.execute('''
            SELECT meals FROM weekly_calendar_data 
            WHERE user_id = %s AND week_start_date = %s
        ''', (user_id, week_start))
        result = cur.fetchone()
        
        if result and result['meals']:
            meals = result['meals']
            for meal_type in ['breakfast', 'lunch', 'dinner', 'snack']:
                slot_key = f"{day_index}-{meal_type}"
                if slot_key in meals and meals[slot_key]:
                    meal_info = meals[slot_key]
                    meal_list = meal_info if isinstance(meal_info, list) else [meal_info]
                    
                    for single_meal in meal_list:
                        if isinstance(single_meal, dict):
                            recipe_id = single_meal.get('recipeId')
                            servings = single_meal.get('servings', 1)
                            if recipe_id:
                                cur.execute('''
                                    SELECT id, title, calories_per_serving 
                                    FROM recipes WHERE id = %s
                                ''', (recipe_id,))
                                recipe = cur.fetchone()
                                if recipe:
                                    total_calories = (recipe['calories_per_serving'] or 0) * servings
                                
                                    # Get recipe image
                                    cur.execute('''
                                        SELECT image_url FROM recipes WHERE id = %s
                                    ''', (recipe_id,))
                                    img_result = cur.fetchone()
                                    image_url = img_result['image_url'] if img_result and img_result['image_url'] else '/static/images/default-recipe.svg'
                                    
                                    recent_meals.append({
                                        'title': recipe['title'],
                                        'meal_type': meal_type.capitalize(),
                                        'calories': int(total_calories),
                                        'date': 'Today',
                                        'image_url': image_url
                                    })
    
    return jsonify({
        'success': True,
        'meals': recent_meals
    })


@dashboard_bp.route('/api/dashboard/upcoming-meals')
@login_required
def get_upcoming_meals():
    """Get upcoming meals for tomorrow."""
    user_id = session['user_id']
    tomorrow = date.today() + timedelta(days=1)
    upcoming_meals = []
    
    with get_db_cursor() as cur:
        days_since_sunday = (tomorrow.weekday() + 1) % 7
        week_start = tomorrow - timedelta(days=days_since_sunday)
        day_index = (tomorrow.weekday() + 1) % 7
        
        cur.execute('''
            SELECT meals FROM weekly_calendar_data 
            WHERE user_id = %s AND week_start_date = %s
        ''', (user_id, week_start))
        result = cur.fetchone()
        
        if result and result['meals']:
            meals = result['meals']
            for meal_type in ['breakfast', 'lunch', 'dinner']:
                slot_key = f"{day_index}-{meal_type}"
                if slot_key in meals and meals[slot_key]:
                    meal_info = meals[slot_key]
                    meal_list = meal_info if isinstance(meal_info, list) else [meal_info]
                    
                    for single_meal in meal_list[:1]:  # Just first meal per type
                        if isinstance(single_meal, dict):
                            recipe_id = single_meal.get('recipeId')
                            servings = single_meal.get('servings', 1)
                            if recipe_id:
                                cur.execute('''
                                    SELECT id, title, calories_per_serving 
                                    FROM recipes WHERE id = %s
                                ''', (recipe_id,))
                                recipe = cur.fetchone()
                                if recipe:
                                    total_calories = (recipe['calories_per_serving'] or 0) * servings
                                    protein = int((total_calories * 0.30) / 4)
                                    
                                    # Get recipe image
                                    cur.execute('''
                                        SELECT image_url FROM recipes WHERE id = %s
                                    ''', (recipe_id,))
                                    img_result = cur.fetchone()
                                    image_url = img_result['image_url'] if img_result and img_result['image_url'] else '/static/images/default-recipe.svg'
                                    
                                    upcoming_meals.append({
                                        'title': recipe['title'],
                                        'meal_type': meal_type.capitalize(),
                                        'calories': int(total_calories),
                                        'protein': protein,
                                        'image_url': image_url
                                    })
    
    return jsonify({
        'success': True,
        'meals': upcoming_meals
    })


@dashboard_bp.route('/api/dashboard/goals-progress')
@login_required
def get_goals_progress():
    """Get user's goals progress."""
    user_id = session['user_id']
    today = date.today()
    
    with get_db_cursor() as cur:
        # Get user's nutrition goals
        cur.execute('''
            SELECT protein_goal FROM user_nutrition_goals 
            WHERE user_id = %s
        ''', (user_id,))
        goals = cur.fetchone()
        protein_goal = goals['protein_goal'] if goals else 150
        
        # Weekly meal planning progress
        days_since_sunday = (today.weekday() + 1) % 7
        week_start = today - timedelta(days=days_since_sunday)
        
        cur.execute('''
            SELECT meals FROM weekly_calendar_data 
            WHERE user_id = %s AND week_start_date = %s
        ''', (user_id, week_start))
        result = cur.fetchone()
        
        days_planned = 0
        if result and result['meals']:
            meals = result['meals']
            for day in range(7):
                day_has_meal = False
                for meal_type in ['breakfast', 'lunch', 'dinner', 'snack']:
                    slot_key = f"{day}-{meal_type}"
                    if slot_key in meals and meals[slot_key]:
                        day_has_meal = True
                        break
                if day_has_meal:
                    days_planned += 1
        
        # Today's protein progress
        day_index = (today.weekday() + 1) % 7
        total_protein = 0
        
        if result and result['meals']:
            meals = result['meals']
            for meal_type in ['breakfast', 'lunch', 'dinner', 'snack']:
                slot_key = f"{day_index}-{meal_type}"
                if slot_key in meals and meals[slot_key]:
                    meal_info = meals[slot_key]
                    meal_list = meal_info if isinstance(meal_info, list) else [meal_info]
                    
                    for single_meal in meal_list:
                        if isinstance(single_meal, dict):
                            recipe_id = single_meal.get('recipeId')
                            servings = single_meal.get('servings', 1)
                            if recipe_id:
                                cur.execute('''
                                    SELECT calories_per_serving 
                                    FROM recipes WHERE id = %s
                                ''', (recipe_id,))
                                recipe = cur.fetchone()
                                if recipe:
                                    total_calories = (recipe['calories_per_serving'] or 0) * servings
                                    # Estimate protein (30% of calories / 4 cal per gram)
                                    total_protein += int((total_calories * 0.30) / 4)
        
        # New recipes this month (simplified - count recent recipes)
        cur.execute('''
            SELECT COUNT(*) as count FROM recipes 
            WHERE user_id = %s 
            AND created_at >= %s
        ''', (user_id, today.replace(day=1)))
        new_recipes_result = cur.fetchone()
        new_recipes = new_recipes_result['count'] if new_recipes_result else 0
        
        # Calorie budget adherence (last 14 days)
        cur.execute('''
            SELECT calorie_goal FROM user_nutrition_goals 
            WHERE user_id = %s
        ''', (user_id,))
        goal_result = cur.fetchone()
        calorie_goal = goal_result['calorie_goal'] if goal_result else 2000
        
        days_within_budget = 0
        for days_ago in range(14):
            check_date = today - timedelta(days=days_ago)
            days_since_sunday = (check_date.weekday() + 1) % 7
            check_week_start = check_date - timedelta(days=days_since_sunday)
            day_idx = (check_date.weekday() + 1) % 7
            
            cur.execute('''
                SELECT meals FROM weekly_calendar_data 
                WHERE user_id = %s AND week_start_date = %s
            ''', (user_id, check_week_start))
            day_result = cur.fetchone()
            
            day_calories = 0
            if day_result and day_result['meals']:
                day_meals = day_result['meals']
                for meal_type in ['breakfast', 'lunch', 'dinner', 'snack']:
                    slot_key = f"{day_idx}-{meal_type}"
                    if slot_key in day_meals and day_meals[slot_key]:
                        meal_info = day_meals[slot_key]
                        meal_list = meal_info if isinstance(meal_info, list) else [meal_info]
                        
                        for single_meal in meal_list:
                            if isinstance(single_meal, dict):
                                recipe_id = single_meal.get('recipeId')
                                servings = single_meal.get('servings', 1)
                                if recipe_id:
                                    cur.execute('''
                                        SELECT calories_per_serving 
                                        FROM recipes WHERE id = %s
                                    ''', (recipe_id,))
                                    recipe = cur.fetchone()
                                    if recipe:
                                        day_calories += (recipe['calories_per_serving'] or 0) * servings
            
            if day_calories > 0 and day_calories <= calorie_goal * 1.1:  # Within 110% of goal
                days_within_budget += 1
        
        return jsonify({
            'success': True,
            'goals': [
                {
                    'name': 'Weekly Meal Planning',
                    'current': days_planned,
                    'target': 7,
                    'unit': 'days'
                },
                {
                    'name': f'Daily Protein Goal ({protein_goal}g)',
                    'current': total_protein,
                    'target': protein_goal,
                    'unit': 'g'
                },
                {
                    'name': 'Try New Recipes',
                    'current': min(new_recipes, 5),
                    'target': 5,
                    'unit': 'this month'
                },
                {
                    'name': 'Stay Within Calorie Budget',
                    'current': days_within_budget,
                    'target': 14,
                    'unit': 'days'
                }
            ]
        })


@dashboard_bp.route('/api/dashboard/weekly-trend')
@login_required
def get_weekly_trend():
    """Get weekly calorie trend for chart."""
    user_id = session['user_id']
    today = date.today()
    days_since_sunday = (today.weekday() + 1) % 7
    week_start = today - timedelta(days=days_since_sunday)
    
    weekly_data = []
    day_names = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']
    
    with get_db_cursor() as cur:
        # Get user's calorie goal for percentage calculation
        cur.execute('''
            SELECT calorie_goal FROM user_nutrition_goals 
            WHERE user_id = %s
        ''', (user_id,))
        goal_result = cur.fetchone()
        calorie_goal = goal_result['calorie_goal'] if goal_result else 2000
        
        cur.execute('''
            SELECT meals FROM weekly_calendar_data 
            WHERE user_id = %s AND week_start_date = %s
        ''', (user_id, week_start))
        result = cur.fetchone()
        
        for day in range(7):
            day_calories = 0
            
            if result and result['meals']:
                meals = result['meals']
                for meal_type in ['breakfast', 'lunch', 'dinner', 'snack']:
                    slot_key = f"{day}-{meal_type}"
                    if slot_key in meals and meals[slot_key]:
                        meal_info = meals[slot_key]
                        meal_list = meal_info if isinstance(meal_info, list) else [meal_info]
                        
                        for single_meal in meal_list:
                            if isinstance(single_meal, dict):
                                recipe_id = single_meal.get('recipeId')
                                servings = single_meal.get('servings', 1)
                                if recipe_id:
                                    cur.execute('''
                                        SELECT calories_per_serving 
                                        FROM recipes WHERE id = %s
                                    ''', (recipe_id,))
                                    recipe = cur.fetchone()
                                    if recipe:
                                        day_calories += (recipe['calories_per_serving'] or 0) * servings
            
            percentage = min(100, int((day_calories / calorie_goal) * 100)) if calorie_goal > 0 else 0
            current_day = week_start + timedelta(days=day)
            is_today = current_day == today
            
            weekly_data.append({
                'day': day_names[day],
                'percentage': percentage,
                'calories': int(day_calories),
                'is_today': is_today
            })
    
    return jsonify({
        'success': True,
        'data': weekly_data
    })
