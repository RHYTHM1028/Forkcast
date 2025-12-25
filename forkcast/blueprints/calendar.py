"""
Calendar Blueprint - Meal planning calendar features.

This blueprint handles:
    - Calendar page view
    - Meal plans CRUD operations
    - Weekly calendar data (auto-save)
"""

import json
from flask import Blueprint, render_template, request, jsonify, session

from ..helpers import login_required, get_current_user
from ..models import get_db_cursor

# Create the blueprint
calendar_bp = Blueprint(
    'calendar',
    __name__,
    template_folder='../templates',
    url_prefix='/calendar'
)


@calendar_bp.route('/')
@login_required
def calendar():
    """Display meal planning calendar page."""
    user = get_current_user()
    return render_template('calendar_template.html', user=user)


# ==================== CALENDAR EVENTS ====================

@calendar_bp.route('/api/events', methods=['GET'])
@login_required
def get_calendar_events():
    """Get calendar events for the logged-in user."""
    user_id = session['user_id']
    with get_db_cursor() as cur:
        cur.execute('''
            SELECT ce.*, r.name as recipe_name 
            FROM calendar_events ce
            LEFT JOIN recipes r ON ce.recipe_id = r.id
            WHERE ce.user_id = %s
            ORDER BY ce.event_date
        ''', (user_id,))
        events = cur.fetchall()
    return jsonify([dict(event) for event in events] if events else [])


@calendar_bp.route('/api/events', methods=['POST'])
@login_required
def add_calendar_event():
    """Add a new calendar event."""
    data = request.get_json()
    user_id = session['user_id']
    
    with get_db_cursor(commit=True) as cur:
        cur.execute('''
            INSERT INTO calendar_events (user_id, recipe_id, event_date, meal_type, notes)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING id
        ''', (user_id, data.get('recipe_id'), data.get('event_date'), 
              data.get('meal_type'), data.get('notes')))
        event_id = cur.fetchone()['id']
    
    return jsonify({'success': True, 'event_id': event_id})


@calendar_bp.route('/api/events/<int:event_id>', methods=['DELETE'])
@login_required
def delete_calendar_event(event_id):
    """Delete a calendar event."""
    user_id = session['user_id']
    with get_db_cursor(commit=True) as cur:
        cur.execute('''
            DELETE FROM calendar_events 
            WHERE id = %s AND user_id = %s
        ''', (event_id, user_id))
    return jsonify({'success': True})


# ==================== MEAL PLANS ====================

@calendar_bp.route('/api/meal-plans', methods=['GET'])
@login_required
def get_meal_plans():
    """Get all saved meal plans for the logged-in user."""
    user_id = session['user_id']
    with get_db_cursor() as cur:
        cur.execute('''
            SELECT id, name, description, week_start_date, created_at, updated_at
            FROM meal_plans 
            WHERE user_id = %s 
            ORDER BY updated_at DESC
        ''', (user_id,))
        plans = cur.fetchall()
    
    result = []
    for plan in plans:
        plan_dict = dict(plan)
        if plan_dict.get('week_start_date'):
            plan_dict['week_start_date'] = plan_dict['week_start_date'].isoformat()
        if plan_dict.get('created_at'):
            plan_dict['created_at'] = plan_dict['created_at'].isoformat()
        if plan_dict.get('updated_at'):
            plan_dict['updated_at'] = plan_dict['updated_at'].isoformat()
        result.append(plan_dict)
    
    return jsonify(result)


@calendar_bp.route('/api/meal-plans/<int:plan_id>', methods=['GET'])
@login_required
def get_meal_plan(plan_id):
    """Get a specific meal plan with its meals."""
    user_id = session['user_id']
    with get_db_cursor() as cur:
        cur.execute('''
            SELECT * FROM meal_plans 
            WHERE id = %s AND user_id = %s
        ''', (plan_id, user_id))
        plan = cur.fetchone()
    
    if not plan:
        return jsonify({'error': 'Meal plan not found'}), 404
    
    plan_dict = dict(plan)
    if plan_dict.get('week_start_date'):
        plan_dict['week_start_date'] = plan_dict['week_start_date'].isoformat()
    if plan_dict.get('created_at'):
        plan_dict['created_at'] = plan_dict['created_at'].isoformat()
    if plan_dict.get('updated_at'):
        plan_dict['updated_at'] = plan_dict['updated_at'].isoformat()
    
    return jsonify(plan_dict)


@calendar_bp.route('/api/meal-plans', methods=['POST'])
@login_required
def save_meal_plan():
    """Save a new meal plan or update existing one."""
    data = request.get_json()
    user_id = session['user_id']
    
    name = data.get('name')
    description = data.get('description', '')
    week_start_date = data.get('week_start_date')
    meals = data.get('meals', {})
    plan_id = data.get('plan_id')  # If updating existing plan
    
    if not name:
        return jsonify({'error': 'Plan name is required'}), 400
    
    with get_db_cursor(commit=True) as cur:
        if plan_id:
            # Update existing plan
            cur.execute('''
                UPDATE meal_plans 
                SET name = %s, description = %s, week_start_date = %s, meals = %s, updated_at = CURRENT_TIMESTAMP
                WHERE id = %s AND user_id = %s
                RETURNING id
            ''', (name, description, week_start_date, json.dumps(meals), plan_id, user_id))
            result = cur.fetchone()
            if not result:
                return jsonify({'error': 'Meal plan not found'}), 404
            return jsonify({'success': True, 'plan_id': plan_id, 'message': 'Meal plan updated successfully'})
        else:
            # Create new plan
            cur.execute('''
                INSERT INTO meal_plans (user_id, name, description, week_start_date, meals)
                VALUES (%s, %s, %s, %s, %s)
                RETURNING id
            ''', (user_id, name, description, week_start_date, json.dumps(meals)))
            new_plan_id = cur.fetchone()['id']
            return jsonify({'success': True, 'plan_id': new_plan_id, 'message': 'Meal plan saved successfully'})


@calendar_bp.route('/api/meal-plans/<int:plan_id>', methods=['DELETE'])
@login_required
def delete_meal_plan(plan_id):
    """Delete a meal plan."""
    user_id = session['user_id']
    with get_db_cursor(commit=True) as cur:
        cur.execute('''
            DELETE FROM meal_plans 
            WHERE id = %s AND user_id = %s
        ''', (plan_id, user_id))
    return jsonify({'success': True})


# ==================== WEEKLY CALENDAR DATA (AUTO-SAVE) ====================

@calendar_bp.route('/api/week/<week_start>', methods=['GET'])
@login_required
def get_week_calendar(week_start):
    """Get calendar data for a specific week."""
    user_id = session['user_id']
    with get_db_cursor() as cur:
        cur.execute('''
            SELECT meals FROM weekly_calendar_data 
            WHERE user_id = %s AND week_start_date = %s
        ''', (user_id, week_start))
        result = cur.fetchone()
    
    if result:
        return jsonify({'success': True, 'meals': result['meals'] or {}})
    return jsonify({'success': True, 'meals': {}})


@calendar_bp.route('/api/week/<week_start>', methods=['POST'])
@login_required
def save_week_calendar(week_start):
    """Auto-save calendar data for a specific week (upsert)."""
    data = request.get_json()
    user_id = session['user_id']
    meals = data.get('meals', {})
    
    with get_db_cursor(commit=True) as cur:
        # Upsert: Insert or update on conflict
        cur.execute('''
            INSERT INTO weekly_calendar_data (user_id, week_start_date, meals)
            VALUES (%s, %s, %s)
            ON CONFLICT (user_id, week_start_date) 
            DO UPDATE SET meals = %s, updated_at = CURRENT_TIMESTAMP
        ''', (user_id, week_start, json.dumps(meals), json.dumps(meals)))
    
    return jsonify({'success': True})


@calendar_bp.route('/api/week/<week_start>/slot', methods=['DELETE'])
@login_required
def delete_calendar_slot(week_start):
    """Delete a specific slot from a week's calendar."""
    data = request.get_json()
    user_id = session['user_id']
    slot_key = data.get('slot_key')
    
    if not slot_key:
        return jsonify({'error': 'slot_key is required'}), 400
    
    with get_db_cursor(commit=True) as cur:
        # Get current meals
        cur.execute('''
            SELECT meals FROM weekly_calendar_data 
            WHERE user_id = %s AND week_start_date = %s
        ''', (user_id, week_start))
        result = cur.fetchone()
        
        if result and result['meals']:
            meals = result['meals']
            if slot_key in meals:
                del meals[slot_key]
                cur.execute('''
                    UPDATE weekly_calendar_data 
                    SET meals = %s, updated_at = CURRENT_TIMESTAMP
                    WHERE user_id = %s AND week_start_date = %s
                ''', (json.dumps(meals), user_id, week_start))
    
    return jsonify({'success': True})


@calendar_bp.route('/api/remove-recipe', methods=['POST'])
@login_required
def remove_recipe_from_calendar():
    """Delete a specific recipe from today's meal slot."""
    from datetime import date, timedelta
    
    data = request.get_json()
    user_id = session['user_id']
    recipe_id = data.get('recipe_id')
    meal_type = data.get('meal_type', '').lower()  # breakfast, lunch, dinner, snack
    target_date_str = data.get('date')  # Optional: specify date, defaults to today
    
    if not recipe_id or not meal_type:
        return jsonify({'error': 'recipe_id and meal_type are required'}), 400
    
    # Parse target date or use today
    if target_date_str:
        target_date = date.fromisoformat(target_date_str)
    else:
        target_date = date.today()
    
    with get_db_cursor(commit=True) as cur:
        # Find all weeks for this user and check which one contains the target date
        cur.execute('''
            SELECT week_start_date, meals FROM weekly_calendar_data 
            WHERE user_id = %s
            ORDER BY week_start_date DESC
        ''', (user_id,))
        all_weeks = cur.fetchall()
        
        for week in all_weeks:
            week_start = week['week_start_date']
            week_end = week_start + timedelta(days=6)
            
            # Check if target date falls within this week
            if week_start <= target_date <= week_end:
                meals = week['meals']
                if not meals:
                    continue
                
                # Calculate day index (0=Sunday for the week)
                # Python weekday(): 0=Monday, 6=Sunday
                # Convert to: 0=Sunday, 6=Saturday using (weekday + 1) % 7
                day_index = (target_date.weekday() + 1) % 7
                slot_key = f"{day_index}-{meal_type}"
                
                if slot_key in meals and isinstance(meals[slot_key], list):
                    # Remove the specific recipe from the array
                    original_length = len(meals[slot_key])
                    meals[slot_key] = [meal for meal in meals[slot_key] 
                                       if meal.get('recipeId') != recipe_id]
                    
                    # Check if anything was removed
                    if len(meals[slot_key]) < original_length:
                        # If the array is now empty, remove the slot entirely
                        if len(meals[slot_key]) == 0:
                            del meals[slot_key]
                        
                        # Update the database
                        cur.execute('''
                            UPDATE weekly_calendar_data 
                            SET meals = %s, updated_at = CURRENT_TIMESTAMP
                            WHERE user_id = %s AND week_start_date = %s
                        ''', (json.dumps(meals), user_id, week_start))
                        
                        return jsonify({'success': True, 'message': 'Recipe removed from calendar'})
    
    return jsonify({'success': False, 'error': 'Recipe not found in calendar'})


@calendar_bp.route('/api/all-weeks', methods=['GET'])
@login_required
def get_all_weeks_calendar():
    """Get all calendar data for the user (for shopping list and calorie tracking)."""
    user_id = session['user_id']
    with get_db_cursor() as cur:
        cur.execute('''
            SELECT week_start_date, meals FROM weekly_calendar_data 
            WHERE user_id = %s 
            ORDER BY week_start_date
        ''', (user_id,))
        results = cur.fetchall()
    
    weeks_data = {}
    for row in results:
        week_key = row['week_start_date'].isoformat() if row['week_start_date'] else None
        if week_key:
            weeks_data[week_key] = row['meals'] or {}
    
    return jsonify({'success': True, 'weeks': weeks_data})
