from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import psycopg2
from psycopg2.extras import RealDictCursor
from functools import wraps
import db

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-this-in-production'

# Database connection function
def get_db_connection():
    conn = psycopg2.connect(
        dbname=db.db_name,
        user=db.db_user,
        password=db.db_pw,
        host=db.db_host
    )
    return conn

# Login required decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to access this page.', 'error')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# Initialize database tables
def init_db():
    conn = get_db_connection()
    cur = conn.cursor()
    
    # Create users table
    cur.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            username VARCHAR(50) UNIQUE NOT NULL,
            email VARCHAR(100) UNIQUE NOT NULL,
            password_hash VARCHAR(255) NOT NULL,
            full_name VARCHAR(100),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    cur.close()
    conn.close()

# Routes
@app.route('/')
def index():
    # If user is logged in, redirect to logged-in home page
    if 'user_id' in session:
        return redirect(url_for('logged_in_home'))
    return render_template('Home.html')

@app.route('/home')
def home():
    # If user is logged in, redirect to logged-in home page
    if 'user_id' in session:
        return redirect(url_for('logged_in_home'))
    return render_template('Home.html')

@app.route('/logged-in-home')
@login_required
def logged_in_home():
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute('SELECT * FROM users WHERE id = %s', (session['user_id'],))
    user = cur.fetchone()
    cur.close()
    conn.close()
    return render_template('logged_in_home.html', user=user)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if 'user_id' in session:
        return redirect(url_for('home'))
    
    if request.method == 'POST':
        # Check if request is JSON (AJAX) or form data
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
        conn = get_db_connection()
        cur = conn.cursor()
        
        cur.execute('SELECT id FROM users WHERE email = %s', (email,))
        existing_user = cur.fetchone()
        
        if existing_user:
            cur.close()
            conn.close()
            message = 'Email already exists.'
            if is_ajax:
                return jsonify({'success': False, 'message': message})
            flash(message, 'error')
            return render_template('signup.html')
        
        # Create new user
        password_hash = generate_password_hash(password)
        
        try:
            cur.execute(
                'INSERT INTO users (username, email, password_hash, full_name) VALUES (%s, %s, %s, %s) RETURNING id',
                (username or email.split('@')[0], email, password_hash, full_name)
            )
            user_id = cur.fetchone()[0]
            conn.commit()
            
            # Log user in
            session['user_id'] = user_id
            session['username'] = username or email.split('@')[0]
            
            if is_ajax:
                return jsonify({'success': True, 'message': 'Account created successfully!'})
            
            flash('Account created successfully! Welcome to Forkcast!', 'success')
            return redirect(url_for('logged_in_home'))
            
        except Exception as e:
            conn.rollback()
            message = 'An error occurred. Please try again.'
            print(f"Error: {e}")
            if is_ajax:
                return jsonify({'success': False, 'message': message})
            flash(message, 'error')
        finally:
            cur.close()
            conn.close()
    
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'user_id' in session:
        return redirect(url_for('home'))
    
    if request.method == 'POST':
        # Check if request is JSON (AJAX) or form data
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
        
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        
        cur.execute('SELECT * FROM users WHERE email = %s', (email,))
        user = cur.fetchone()
        
        cur.close()
        conn.close()
        
        if user and check_password_hash(user['password_hash'], password):
            session['user_id'] = user['id']
            session['username'] = user['username']
            
            if remember:
                session.permanent = True
            
            if is_ajax:
                return jsonify({'success': True, 'message': 'Login successful!'})
            
            flash('Login successful! Welcome back!', 'success')
            return redirect(url_for('logged_in_home'))
        else:
            message = 'Invalid email or password.'
            if is_ajax:
                return jsonify({'success': False, 'message': message})
            flash(message, 'error')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'success')
    return redirect(url_for('home'))

@app.route('/dashboard')
@login_required
def dashboard():
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute('SELECT * FROM users WHERE id = %s', (session['user_id'],))
    user = cur.fetchone()
    cur.close()
    conn.close()
    return render_template('dashboard.html', user=user)

@app.route('/profile')
@login_required
def profile():
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute('SELECT * FROM users WHERE id = %s', (session['user_id'],))
    user = cur.fetchone()
    cur.close()
    conn.close()
    return render_template('profile_template.html', user=user)

@app.route('/recipes')
@login_required
def recipes():
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute('SELECT * FROM users WHERE id = %s', (session['user_id'],))
    user = cur.fetchone()
    cur.close()
    conn.close()
    return render_template('recipe.html', user=user)

@app.route('/calendar')
@login_required
def calendar():
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute('SELECT * FROM users WHERE id = %s', (session['user_id'],))
    user = cur.fetchone()
    cur.close()
    conn.close()
    return render_template('calendar_template.html', user=user)

@app.route('/calorie-tracker')
@login_required
def calorie_tracker():
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute('SELECT * FROM users WHERE id = %s', (session['user_id'],))
    user = cur.fetchone()
    cur.close()
    conn.close()
    return render_template('calorie_tracker.html', user=user)

@app.route('/shopping-list')
@login_required
def shopping_list():
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute('SELECT * FROM users WHERE id = %s', (session['user_id'],))
    user = cur.fetchone()
    cur.close()
    conn.close()
    return render_template('shopping_list.html', user=user)

@app.route('/notifications')
@login_required
def notifications():
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute('SELECT * FROM users WHERE id = %s', (session['user_id'],))
    user = cur.fetchone()
    cur.close()
    conn.close()
    return render_template('notification.html', user=user)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
