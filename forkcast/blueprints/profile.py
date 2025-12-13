"""
Profile Blueprint - User profile management.

This blueprint handles:
    - User dashboard
    - Profile viewing
    - Profile editing
    - Password change
    - Account deletion
"""

import os
import uuid
from flask import (
    Blueprint, render_template, request, redirect, 
    url_for, flash, session, jsonify, current_app
)
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename

from ..models import get_db_cursor
from ..helpers import login_required, get_current_user, allowed_file

# Create the blueprint
profile_bp = Blueprint(
    'profile',
    __name__,
    template_folder='../templates'
)


@profile_bp.route('/dashboard')
@login_required
def dashboard():
    """User dashboard page."""
    user = get_current_user()
    return render_template('dashboard.html', user=user)


@profile_bp.route('/profile')
@login_required
def profile():
    """
    User profile page with stats.
    Shows user information and recipe statistics.
    """
    with get_db_cursor() as cur:
        cur.execute('SELECT * FROM users WHERE id = %s', (session['user_id'],))
        user = cur.fetchone()
        
        # Get user stats
        cur.execute('SELECT COUNT(*) as count FROM recipes WHERE user_id = %s', (session['user_id'],))
        recipes_count = cur.fetchone()['count']
        
        cur.execute('SELECT COUNT(*) as count FROM recipes WHERE user_id = %s AND is_favorite = true', (session['user_id'],))
        favorites_count = cur.fetchone()['count']
    
    return render_template('profile_template.html', user=user, recipes_count=recipes_count, favorites_count=favorites_count)


@profile_bp.route('/edit-profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    """
    Edit user profile page.
    
    GET: Display edit form
    POST: Process profile updates
    """
    if request.method == 'POST':
        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest' or request.is_json
        
        full_name = request.form.get('full_name', '').strip()
        email = request.form.get('email', '').strip()
        bio = request.form.get('bio', '').strip()
        
        if not email:
            message = 'Email is required.'
            if is_ajax:
                return jsonify({'success': False, 'message': message})
            flash(message, 'error')
            return redirect(url_for('profile.edit_profile'))
        
        # Check if email is already taken by another user
        with get_db_cursor() as cur:
            cur.execute('SELECT id FROM users WHERE email = %s AND id != %s', (email, session['user_id']))
            existing_user = cur.fetchone()
        
        if existing_user:
            message = 'Email already exists.'
            if is_ajax:
                return jsonify({'success': False, 'message': message})
            flash(message, 'error')
            return redirect(url_for('profile.edit_profile'))
        
        # Handle profile photo upload
        profile_image_url = None
        if 'profile_photo' in request.files:
            file = request.files['profile_photo']
            if file and file.filename and allowed_file(file.filename):
                # Generate unique filename
                filename = secure_filename(file.filename)
                unique_filename = f"{uuid.uuid4().hex}_{filename}"
                
                # Create profiles upload directory if it doesn't exist
                profiles_dir = os.path.join(current_app.config['UPLOAD_FOLDER'], 'profiles')
                os.makedirs(profiles_dir, exist_ok=True)
                
                # Save the file
                file_path = os.path.join(profiles_dir, unique_filename)
                file.save(file_path)
                profile_image_url = f"/static/uploads/profiles/{unique_filename}"
        
        # Update user profile
        try:
            with get_db_cursor(commit=True) as cur:
                if profile_image_url:
                    cur.execute('''
                        UPDATE users 
                        SET full_name = %s, email = %s, bio = %s, profile_image = %s, updated_at = CURRENT_TIMESTAMP
                        WHERE id = %s
                    ''', (full_name, email, bio, profile_image_url, session['user_id']))
                else:
                    cur.execute('''
                        UPDATE users 
                        SET full_name = %s, email = %s, bio = %s, updated_at = CURRENT_TIMESTAMP
                        WHERE id = %s
                    ''', (full_name, email, bio, session['user_id']))
            
            if is_ajax:
                return jsonify({'success': True, 'message': 'Profile updated successfully!'})
            
            flash('Profile updated successfully!', 'success')
            return redirect(url_for('profile.profile'))
            
        except Exception as e:
            message = 'An error occurred. Please try again.'
            print(f"Error: {e}")
            if is_ajax:
                return jsonify({'success': False, 'message': message})
            flash(message, 'error')
    
    # GET request - show form
    user = get_current_user()
    return render_template('edit_profile_template.html', user=user)


@profile_bp.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    """
    Change user password page.
    
    GET: Display password change form
    POST: Process password change
    """
    if request.method == 'POST':
        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest' or request.is_json
        
        current_password = request.form.get('current_password', '').strip()
        new_password = request.form.get('new_password', '').strip()
        confirm_password = request.form.get('confirm_password', '').strip()
        
        if not current_password or not new_password or not confirm_password:
            message = 'All fields are required.'
            if is_ajax:
                return jsonify({'success': False, 'message': message})
            flash(message, 'error')
            return redirect(url_for('profile.change_password'))
        
        if new_password != confirm_password:
            message = 'New passwords do not match.'
            if is_ajax:
                return jsonify({'success': False, 'message': message})
            flash(message, 'error')
            return redirect(url_for('profile.change_password'))
        
        if len(new_password) < 6:
            message = 'Password must be at least 6 characters long.'
            if is_ajax:
                return jsonify({'success': False, 'message': message})
            flash(message, 'error')
            return redirect(url_for('profile.change_password'))
        
        # Verify current password
        with get_db_cursor() as cur:
            cur.execute('SELECT password_hash FROM users WHERE id = %s', (session['user_id'],))
            user = cur.fetchone()
        
        if not user or not check_password_hash(user['password_hash'], current_password):
            message = 'Current password is incorrect.'
            if is_ajax:
                return jsonify({'success': False, 'message': message})
            flash(message, 'error')
            return redirect(url_for('profile.change_password'))
        
        # Update password
        try:
            new_password_hash = generate_password_hash(new_password)
            with get_db_cursor(commit=True) as cur:
                cur.execute('''
                    UPDATE users 
                    SET password_hash = %s, updated_at = CURRENT_TIMESTAMP
                    WHERE id = %s
                ''', (new_password_hash, session['user_id']))
            
            if is_ajax:
                return jsonify({'success': True, 'message': 'Password changed successfully!'})
            
            flash('Password changed successfully!', 'success')
            return redirect(url_for('profile.profile'))
            
        except Exception as e:
            message = 'An error occurred. Please try again.'
            print(f"Error: {e}")
            if is_ajax:
                return jsonify({'success': False, 'message': message})
            flash(message, 'error')
    
    # GET request - show form
    user = get_current_user()
    return render_template('change_password_template.html', user=user)


@profile_bp.route('/delete-account', methods=['POST'])
@login_required
def delete_account():
    """
    Delete user account and all associated data.
    Requires password confirmation.
    """
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest' or request.is_json
    
    password = request.form.get('password', '').strip()
    
    if not password:
        message = 'Password is required to delete account.'
        if is_ajax:
            return jsonify({'success': False, 'message': message})
        flash(message, 'error')
        return redirect(url_for('profile.profile'))
    
    user_id = session['user_id']
    
    # Verify password
    with get_db_cursor() as cur:
        cur.execute('SELECT password_hash FROM users WHERE id = %s', (user_id,))
        user = cur.fetchone()
    
    if not user or not check_password_hash(user['password_hash'], password):
        message = 'Incorrect password.'
        if is_ajax:
            return jsonify({'success': False, 'message': message})
        flash(message, 'error')
        return redirect(url_for('profile.profile'))
    
    try:
        with get_db_cursor(commit=True) as cur:
            # Helper function to check if table exists
            def table_exists(table_name):
                cur.execute("""
                    SELECT EXISTS (
                        SELECT FROM information_schema.tables 
                        WHERE table_name = %s
                    )
                """, (table_name,))
                return cur.fetchone()['exists']
            
            # Delete user's ratings/reviews
            if table_exists('recipe_ratings'):
                cur.execute('DELETE FROM recipe_ratings WHERE user_id = %s', (user_id,))
            
            # Delete user's recipes
            if table_exists('recipes'):
                cur.execute('DELETE FROM recipes WHERE user_id = %s', (user_id,))
            
            # Delete calendar events if table exists
            if table_exists('calendar_events'):
                cur.execute('DELETE FROM calendar_events WHERE user_id = %s', (user_id,))
            
            # Delete calorie logs if table exists
            if table_exists('calorie_logs'):
                cur.execute('DELETE FROM calorie_logs WHERE user_id = %s', (user_id,))
            
            # Delete shopping list items if table exists
            if table_exists('shopping_list'):
                cur.execute('DELETE FROM shopping_list WHERE user_id = %s', (user_id,))
            
            # Delete notifications if table exists
            if table_exists('notifications'):
                cur.execute('DELETE FROM notifications WHERE user_id = %s', (user_id,))
            
            # Finally, delete the user
            cur.execute('DELETE FROM users WHERE id = %s', (user_id,))
        
        # Clear session
        session.clear()
        
        if is_ajax:
            return jsonify({'success': True, 'message': 'Account deleted successfully.', 'redirect': url_for('main.home')})
        
        flash('Your account has been deleted.', 'success')
        return redirect(url_for('main.home'))
        
    except Exception as e:
        print(f"Error deleting account: {e}")
        message = 'An error occurred while deleting your account. Please try again.'
        if is_ajax:
            return jsonify({'success': False, 'message': message})
        flash(message, 'error')
        return redirect(url_for('profile.profile'))
