"""
Shopping List Blueprint - Shopping list management.

This blueprint handles:
    - Shopping list page view
    - Shopping list item CRUD operations
"""

from flask import Blueprint, render_template, request, jsonify, session

from ..helpers import login_required, get_current_user
from ..models import get_db_cursor

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
