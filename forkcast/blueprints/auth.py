"""
Auth Blueprint - Authentication routes.

This blueprint handles:
    - User registration (signup)
    - User login
    - User logout
"""

from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify
from werkzeug.security import generate_password_hash, check_password_hash

from ..models import get_db_cursor

# Create the blueprint
auth_bp = Blueprint(
    'auth',
    __name__,
    template_folder='../templates'
)


@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    """
    User registration page.
    
    GET: Display signup form
    POST: Process registration
    """
    if 'user_id' in session:
        return redirect(url_for('main.home'))
    
    if request.method == 'POST':
        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest' or request.is_json
        
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '').strip()
        full_name = request.form.get('full_name', '').strip()
        
        # Validation
        if not email or not password:
            message = 'Email and password are required.'
            if is_ajax:
                return jsonify({'success': False, 'message': message})
            flash(message, 'error')
            return render_template('signup.html')
        
        if len(password) < 6:
            message = 'Password must be at least 6 characters long.'
            if is_ajax:
                return jsonify({'success': False, 'message': message})
            flash(message, 'error')
            return render_template('signup.html')
        
        # Check if user already exists
        with get_db_cursor() as cur:
            cur.execute('SELECT id FROM users WHERE email = %s', (email,))
            existing_user = cur.fetchone()
        
        if existing_user:
            message = 'Email already exists.'
            if is_ajax:
                return jsonify({'success': False, 'message': message})
            flash(message, 'error')
            return render_template('signup.html')
        
        # Create new user
        password_hash = generate_password_hash(password)
        
        try:
            with get_db_cursor(commit=True) as cur:
                cur.execute(
                    'INSERT INTO users (username, email, password_hash, full_name) VALUES (%s, %s, %s, %s) RETURNING id',
                    (username or email.split('@')[0], email, password_hash, full_name)
                )
                user_id = cur.fetchone()['id']
            
            # Log user in
            session['user_id'] = user_id
            session['username'] = username or email.split('@')[0]
            
            if is_ajax:
                return jsonify({'success': True, 'message': 'Account created successfully!'})
            
            flash('Account created successfully! Welcome to Forkcast!', 'success')
            return redirect(url_for('main.logged_in_home'))
            
        except Exception as e:
            message = 'An error occurred. Please try again.'
            print(f"Error: {e}")
            if is_ajax:
                return jsonify({'success': False, 'message': message})
            flash(message, 'error')
    
    return render_template('signup.html')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """
    User login page.
    
    GET: Display login form
    POST: Process login
    """
    if 'user_id' in session:
        return redirect(url_for('main.home'))
    
    if request.method == 'POST':
        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest' or request.is_json
        
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '').strip()
        remember = request.form.get('remember') == 'on'
        
        if not email or not password:
            message = 'Email and password are required.'
            if is_ajax:
                return jsonify({'success': False, 'message': message})
            flash(message, 'error')
            return render_template('login.html')
        
        with get_db_cursor() as cur:
            cur.execute('SELECT * FROM users WHERE email = %s', (email,))
            user = cur.fetchone()
        
        if user and check_password_hash(user['password_hash'], password):
            session['user_id'] = user['id']
            session['username'] = user['username']
            
            if remember:
                session.permanent = True
            
            if is_ajax:
                return jsonify({'success': True, 'message': 'Login successful!'})
            
            flash('Login successful! Welcome back!', 'success')
            return redirect(url_for('main.logged_in_home'))
        else:
            message = 'Invalid email or password.'
            if is_ajax:
                return jsonify({'success': False, 'message': message})
            flash(message, 'error')
    
    return render_template('login.html')


@auth_bp.route('/logout')
def logout():
    """
    Log user out and clear session.
    """
    session.clear()
    flash('You have been logged out.', 'success')
    return redirect(url_for('main.home'))
