"""
Shopping List Blueprint - Shopping list management.

This blueprint handles:
    - Shopping list page view
    - Shopping list item CRUD operations
    - Auto-generation from weekly meal plan
    - Ingredient aggregation and categorization
"""

from flask import Blueprint, render_template, request, jsonify, session
from datetime import date, timedelta

from ..helpers import login_required, get_current_user
from ..models import get_db_cursor
from ..ingredient_parser import parse_ingredient, aggregate_ingredients, format_quantity

# Create the blueprint
shopping_list_bp = Blueprint(
    'shopping_list',
    __name__,
    template_folder='../templates',
    url_prefix='/shopping-list'
)


@shopping_list_bp.route('/')
@login_required
def shopping_list():
    """Display shopping list page."""
    user = get_current_user()
    return render_template('shopping_list.html', user=user)


@shopping_list_bp.route('/api/items', methods=['GET'])
@login_required
def get_shopping_list():
    """Get shopping list items for the logged-in user."""
    user_id = session['user_id']
    with get_db_cursor() as cur:
        cur.execute('''
            SELECT * FROM shopping_list 
            WHERE user_id = %s 
            ORDER BY is_checked, created_at DESC
        ''', (user_id,))
        items = cur.fetchall()
    return jsonify([dict(item) for item in items] if items else [])


@shopping_list_bp.route('/api/items', methods=['POST'])
@login_required
def add_shopping_item():
    """Add an item to shopping list."""
    data = request.get_json()
    user_id = session['user_id']
    
    with get_db_cursor(commit=True) as cur:
        cur.execute('''
            INSERT INTO shopping_list (user_id, item_name, quantity, unit, category)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING id
        ''', (user_id, data.get('item_name'), data.get('quantity'),
              data.get('unit'), data.get('category')))
        item_id = cur.fetchone()['id']
    
    return jsonify({'success': True, 'item_id': item_id})


@shopping_list_bp.route('/api/items/<int:item_id>', methods=['PUT'])
@login_required
def update_shopping_item(item_id):
    """Update a shopping list item (toggle checked status)."""
    data = request.get_json()
    user_id = session['user_id']
    
    with get_db_cursor(commit=True) as cur:
        cur.execute('''
            UPDATE shopping_list 
            SET is_checked = %s
            WHERE id = %s AND user_id = %s
        ''', (data.get('is_checked'), item_id, user_id))
    
    return jsonify({'success': True})


@shopping_list_bp.route('/api/items/<int:item_id>', methods=['DELETE'])
@login_required
def delete_shopping_item(item_id):
    """Delete a shopping list item."""
    user_id = session['user_id']
    with get_db_cursor(commit=True) as cur:
        cur.execute('''
            DELETE FROM shopping_list 
            WHERE id = %s AND user_id = %s
        ''', (item_id, user_id))
    return jsonify({'success': True})


@shopping_list_bp.route('/api/clear-checked', methods=['DELETE'])
@login_required
def clear_checked_items():
    """Clear all checked items from shopping list."""
    user_id = session['user_id']
    with get_db_cursor(commit=True) as cur:
        cur.execute('''
            DELETE FROM shopping_list 
            WHERE user_id = %s AND is_checked = TRUE
        ''', (user_id,))
    return jsonify({'success': True})


@shopping_list_bp.route('/api/generate-from-meal-plan', methods=['POST'])
@login_required
def generate_from_meal_plan():
    """
    Generate shopping list from weekly meal plan.
    Aggregates ingredients from all recipes in the current week.
    
    Request body options:
        - clear_existing: bool (default True) - Clear auto-generated items before adding
        - selected_days: list of ints (0-6) - Days to include (0=Sunday, 6=Saturday)
        - selected_meals: list of strings - Meal types to include (breakfast, lunch, dinner, snack)
    """
    user_id = session['user_id']
    data = request.get_json() or {}
    
    # Get date range (default to current week)
    today = date.today()
    days_since_sunday = (today.weekday() + 1) % 7
    week_start = today - timedelta(days=days_since_sunday)
    
    # Option to clear existing auto-generated items
    clear_existing = data.get('clear_existing', True)
    
    # Get selected days (default to all days 0-6)
    selected_days = data.get('selected_days', list(range(7)))
    
    # Get selected meal types (default to all)
    selected_meals = data.get('selected_meals', ['breakfast', 'lunch', 'dinner', 'snack'])
    
    with get_db_cursor(commit=True) as cur:
        # Clear existing auto-generated items if requested
        if clear_existing:
            cur.execute('''
                DELETE FROM shopping_list 
                WHERE user_id = %s AND source = 'auto'
            ''', (user_id,))
        
        # Get all recipes from the weekly meal plan
        cur.execute('''
            SELECT meals FROM weekly_calendar_data 
            WHERE user_id = %s AND week_start_date = %s
        ''', (user_id, week_start))
        result = cur.fetchone()
        
        if not result or not result['meals']:
            return jsonify({
                'success': False,
                'message': 'No meals planned for this week'
            })
        
        meals = result['meals']
        recipe_ids = set()
        recipe_servings = {}
        
        # Extract recipe IDs and servings only from selected days and meal types
        for day in selected_days:
            for meal_type in selected_meals:
                slot_key = f"{day}-{meal_type}"
                if slot_key in meals and meals[slot_key]:
                    meal_info = meals[slot_key]
                    meal_list = meal_info if isinstance(meal_info, list) else [meal_info]
                    
                    for single_meal in meal_list:
                        if isinstance(single_meal, dict):
                            recipe_id = single_meal.get('recipeId')
                            servings = single_meal.get('servings', 1)
                            if recipe_id:
                                recipe_ids.add(recipe_id)
                                # Track total servings needed for each recipe
                                if recipe_id in recipe_servings:
                                    recipe_servings[recipe_id] += servings
                                else:
                                    recipe_servings[recipe_id] = servings
        
        if not recipe_ids:
            return jsonify({
                'success': False,
                'message': 'No recipes found in meal plan'
            })
        
        # Fetch all recipes with their ingredients
        placeholders = ','.join(['%s'] * len(recipe_ids))
        cur.execute(f'''
            SELECT id, title, ingredients, servings 
            FROM recipes 
            WHERE id IN ({placeholders})
        ''', tuple(recipe_ids))
        recipes = cur.fetchall()
        
        # Parse and aggregate ingredients
        all_ingredients = []
        
        for recipe in recipes:
            recipe_id = recipe['id']
            ingredients_text = recipe['ingredients']
            recipe_base_servings = recipe['servings'] or 1
            total_servings_needed = recipe_servings.get(recipe_id, 1)
            
            # Calculate scaling factor
            scale_factor = total_servings_needed / recipe_base_servings
            
            # Parse each ingredient line
            for line in ingredients_text.split('\n'):
                parsed = parse_ingredient(line)
                if parsed:
                    # Scale quantity based on servings needed
                    parsed['quantity'] *= scale_factor
                    parsed['recipe_id'] = recipe_id
                    parsed['recipe_title'] = recipe['title']
                    all_ingredients.append(parsed)
        
        # Aggregate ingredients
        aggregated = aggregate_ingredients(all_ingredients)
        
        # Insert aggregated ingredients into shopping list
        items_added = 0
        for ing in aggregated:
            formatted_qty = format_quantity(ing['quantity'])
            
            cur.execute('''
                INSERT INTO shopping_list 
                (user_id, item_name, quantity, unit, category, source, is_checked)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            ''', (user_id, ing['name'], formatted_qty, ing['unit'], 
                  ing['category'], 'auto', False))
            items_added += 1
        
        # Build descriptive message
        day_names = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']
        selected_day_names = [day_names[d] for d in selected_days]
        
        if len(selected_days) == 7 and len(selected_meals) == 4:
            selection_info = "entire week"
        else:
            days_str = ', '.join(selected_day_names) if len(selected_days) <= 3 else f"{len(selected_days)} days"
            meals_str = ', '.join(selected_meals) if len(selected_meals) <= 2 else f"{len(selected_meals)} meal types"
            selection_info = f"{days_str} ({meals_str})"
        
        return jsonify({
            'success': True,
            'message': f'Added {items_added} items from {selection_info}',
            'items_added': items_added,
            'recipes_found': len(recipe_ids)
        })


@shopping_list_bp.route('/api/items/<int:item_id>/edit', methods=['PUT'])
@login_required
def edit_shopping_item(item_id):
    """Edit a shopping list item (quantity, unit, name)."""
    data = request.get_json()
    user_id = session['user_id']
    
    with get_db_cursor(commit=True) as cur:
        cur.execute('''
            UPDATE shopping_list 
            SET item_name = %s, quantity = %s, unit = %s, category = %s
            WHERE id = %s AND user_id = %s
        ''', (data.get('item_name'), data.get('quantity'), 
              data.get('unit'), data.get('category'), item_id, user_id))
    
    return jsonify({'success': True})


@shopping_list_bp.route('/api/items/by-category', methods=['GET'])
@login_required
def get_items_by_category():
    """Get shopping list items grouped by category."""
    user_id = session['user_id']
    
    with get_db_cursor() as cur:
        cur.execute('''
            SELECT * FROM shopping_list 
            WHERE user_id = %s 
            ORDER BY 
                CASE 
                    WHEN category = 'Vegetables' THEN 1
                    WHEN category = 'Fruits' THEN 2
                    WHEN category = 'Meat & Seafood' THEN 3
                    WHEN category = 'Dairy & Eggs' THEN 4
                    WHEN category = 'Grains & Pasta' THEN 5
                    WHEN category = 'Pantry' THEN 6
                    WHEN category = 'Herbs & Spices' THEN 7
                    WHEN category = 'Baking' THEN 8
                    WHEN category = 'Nuts & Seeds' THEN 9
                    ELSE 10
                END,
                is_checked, 
                created_at DESC
        ''', (user_id,))
        items = cur.fetchall()
    
    # Group by category
    grouped = {}
    for item in items:
        category = item['category'] or 'Other'
        if category not in grouped:
            grouped[category] = []
        grouped[category].append(dict(item))
    
    return jsonify({
        'success': True,
        'items_by_category': grouped
    })


@shopping_list_bp.route('/api/clear-all', methods=['DELETE'])
@login_required
def clear_all_items():
    """Clear all items from shopping list."""
    user_id = session['user_id']
    with get_db_cursor(commit=True) as cur:
        cur.execute('''
            DELETE FROM shopping_list 
            WHERE user_id = %s
        ''', (user_id,))
    return jsonify({'success': True})
