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
    
    # Get user stats
    cur.execute('SELECT COUNT(*) as count FROM recipes WHERE user_id = %s', (session['user_id'],))
    recipes_count = cur.fetchone()['count']
    
    cur.execute('SELECT COUNT(*) as count FROM recipes WHERE user_id = %s AND is_favorite = true', (session['user_id'],))
    favorites_count = cur.fetchone()['count']
    
    cur.close()
    conn.close()
    return render_template('profile_template.html', user=user, recipes_count=recipes_count, favorites_count=favorites_count)

@app.route('/edit-profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
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
            return redirect(url_for('edit_profile'))
        
        # Check if email is already taken by another user
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        
        cur.execute('SELECT id FROM users WHERE email = %s AND id != %s', (email, session['user_id']))
        existing_user = cur.fetchone()
        
        if existing_user:
            cur.close()
            conn.close()
            message = 'Email already exists.'
            if is_ajax:
                return jsonify({'success': False, 'message': message})
            flash(message, 'error')
            return redirect(url_for('edit_profile'))
        
        # Update user profile
        try:
            cur.execute('''
                UPDATE users 
                SET full_name = %s, email = %s, bio = %s, updated_at = CURRENT_TIMESTAMP
                WHERE id = %s
            ''', (full_name, email, bio, session['user_id']))
            conn.commit()
            
            if is_ajax:
                return jsonify({'success': True, 'message': 'Profile updated successfully!'})
            
            flash('Profile updated successfully!', 'success')
            return redirect(url_for('profile'))
            
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
    
    # GET request - show form
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute('SELECT * FROM users WHERE id = %s', (session['user_id'],))
    user = cur.fetchone()
    cur.close()
    conn.close()
    return render_template('edit_profile_template.html', user=user)

@app.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
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
            return redirect(url_for('change_password'))
        
        if new_password != confirm_password:
            message = 'New passwords do not match.'
            if is_ajax:
                return jsonify({'success': False, 'message': message})
            flash(message, 'error')
            return redirect(url_for('change_password'))
        
        if len(new_password) < 6:
            message = 'Password must be at least 6 characters long.'
            if is_ajax:
                return jsonify({'success': False, 'message': message})
            flash(message, 'error')
            return redirect(url_for('change_password'))
        
        # Verify current password
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        
        cur.execute('SELECT password_hash FROM users WHERE id = %s', (session['user_id'],))
        user = cur.fetchone()
        
        if not user or not check_password_hash(user['password_hash'], current_password):
            cur.close()
            conn.close()
            message = 'Current password is incorrect.'
            if is_ajax:
                return jsonify({'success': False, 'message': message})
            flash(message, 'error')
            return redirect(url_for('change_password'))
        
        # Update password
        try:
            new_password_hash = generate_password_hash(new_password)
            cur.execute('''
                UPDATE users 
                SET password_hash = %s, updated_at = CURRENT_TIMESTAMP
                WHERE id = %s
            ''', (new_password_hash, session['user_id']))
            conn.commit()
            
            if is_ajax:
                return jsonify({'success': True, 'message': 'Password changed successfully!'})
            
            flash('Password changed successfully!', 'success')
            return redirect(url_for('profile'))
            
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
    
    # GET request - show form
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute('SELECT * FROM users WHERE id = %s', (session['user_id'],))
    user = cur.fetchone()
    cur.close()
    conn.close()
    return render_template('change_password_template.html', user=user)

@app.route('/recipes')
@login_required
def recipes():
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    
    # Get all public recipes with ratings and author info
    cur.execute('''
        SELECT r.*, r.calories_per_serving as calories, u.username, u.full_name,
               COALESCE(AVG(rr.rating), 0) as avg_rating,
               COUNT(DISTINCT rr.id) as rating_count
        FROM recipes r
        JOIN users u ON r.user_id = u.id
        LEFT JOIN recipe_ratings rr ON r.id = rr.recipe_id
        WHERE r.is_public = true
        GROUP BY r.id, u.username, u.full_name
        ORDER BY r.created_at DESC
    ''')
    all_recipes = cur.fetchall()
    
    cur.execute('SELECT * FROM users WHERE id = %s', (session['user_id'],))
    user = cur.fetchone()
    
    cur.close()
    conn.close()
    return render_template('recipe.html', user=user, recipes=all_recipes)

@app.route('/my-recipes')
@login_required
def my_recipes():
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    
    # Get user's recipes
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
    user_recipes = cur.fetchall()
    
    cur.execute('SELECT * FROM users WHERE id = %s', (session['user_id'],))
    user = cur.fetchone()
    
    cur.close()
    conn.close()
    return render_template('my_recipes.html', user=user, recipes=user_recipes)

@app.route('/api/recipes', methods=['GET'])
@login_required
def get_recipes():
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    
    recipe_type = request.args.get('type', 'all')
    
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
            SELECT r.*, r.calories_per_serving as calories, u.username, u.full_name,
                   COALESCE(AVG(rr.rating), 0) as avg_rating,
                   COUNT(DISTINCT rr.id) as rating_count
            FROM recipes r
            JOIN users u ON r.user_id = u.id
            LEFT JOIN recipe_ratings rr ON r.id = rr.recipe_id
            WHERE r.is_public = true
            GROUP BY r.id, u.username, u.full_name
            ORDER BY r.created_at DESC
        ''')
    
    recipes = cur.fetchall()
    cur.close()
    conn.close()
    
    return jsonify({'success': True, 'recipes': recipes})

@app.route('/api/recipes/<int:recipe_id>', methods=['GET'])
@login_required
def get_recipe(recipe_id):
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    
    cur.execute('''
        SELECT r.*, r.calories_per_serving as calories, u.username, u.full_name,
               COALESCE(AVG(rr.rating), 0) as avg_rating,
               COUNT(DISTINCT rr.id) as rating_count
        FROM recipes r
        JOIN users u ON r.user_id = u.id
        LEFT JOIN recipe_ratings rr ON r.id = rr.recipe_id
        WHERE r.id = %s
        GROUP BY r.id, u.username, u.full_name
    ''', (recipe_id,))
    recipe = cur.fetchone()
    
    if not recipe:
        cur.close()
        conn.close()
        return jsonify({'success': False, 'message': 'Recipe not found'}), 404
    
    # Get user's rating if exists
    cur.execute('SELECT rating, review FROM recipe_ratings WHERE recipe_id = %s AND user_id = %s', 
                (recipe_id, session['user_id']))
    user_rating = cur.fetchone()
    
    cur.close()
    conn.close()
    
    return jsonify({
        'success': True, 
        'recipe': recipe,
        'user_rating': user_rating
    })

@app.route('/api/recipes', methods=['POST'])
@login_required
def create_recipe():
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
    is_public = request.form.get('is_public', 'true') == 'true'
    
    if not title or not ingredients or not instructions:
        message = 'Title, ingredients, and instructions are required.'
        if is_ajax:
            return jsonify({'success': False, 'message': message})
        flash(message, 'error')
        return redirect(url_for('my_recipes'))
    
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    
    try:
        cur.execute('''
            INSERT INTO recipes (user_id, title, description, ingredients, instructions,
                               prep_time, cook_time, servings, calories_per_serving,
                               category, cuisine, difficulty, is_public)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING id
        ''', (session['user_id'], title, description, ingredients, instructions,
              prep_time, cook_time, servings, calories, category, cuisine, difficulty, is_public))
        
        recipe_id = cur.fetchone()['id']
        conn.commit()
        
        if is_ajax:
            return jsonify({'success': True, 'message': 'Recipe created successfully!', 'recipe_id': recipe_id})
        
        flash('Recipe created successfully!', 'success')
        return redirect(url_for('my_recipes'))
        
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
    
    return redirect(url_for('my_recipes'))

@app.route('/api/recipes/<int:recipe_id>', methods=['PUT', 'POST'])
@login_required
def update_recipe(recipe_id):
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest' or request.is_json
    
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    
    # Check if user owns this recipe
    cur.execute('SELECT user_id FROM recipes WHERE id = %s', (recipe_id,))
    recipe = cur.fetchone()
    
    if not recipe or recipe['user_id'] != session['user_id']:
        cur.close()
        conn.close()
        message = 'Recipe not found or you do not have permission to edit it.'
        if is_ajax:
            return jsonify({'success': False, 'message': message}), 403
        flash(message, 'error')
        return redirect(url_for('my_recipes'))
    
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
    is_public = request.form.get('is_public', 'true') == 'true'
    
    try:
        cur.execute('''
            UPDATE recipes 
            SET title = %s, description = %s, ingredients = %s, instructions = %s,
                prep_time = %s, cook_time = %s, servings = %s, calories_per_serving = %s,
                category = %s, cuisine = %s, difficulty = %s, is_public = %s,
                updated_at = CURRENT_TIMESTAMP
            WHERE id = %s
        ''', (title, description, ingredients, instructions, prep_time, cook_time,
              servings, calories, category, cuisine, difficulty, is_public, recipe_id))
        
        conn.commit()
        
        if is_ajax:
            return jsonify({'success': True, 'message': 'Recipe updated successfully!'})
        
        flash('Recipe updated successfully!', 'success')
        return redirect(url_for('my_recipes'))
        
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
    
    return redirect(url_for('my_recipes'))

@app.route('/api/recipes/<int:recipe_id>', methods=['DELETE'])
@login_required
def delete_recipe(recipe_id):
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    
    # Check if user owns this recipe
    cur.execute('SELECT user_id, title FROM recipes WHERE id = %s', (recipe_id,))
    recipe = cur.fetchone()
    
    if not recipe or recipe['user_id'] != session['user_id']:
        cur.close()
        conn.close()
        return jsonify({'success': False, 'message': 'Recipe not found or you do not have permission to delete it.'}), 403
    
    try:
        cur.execute('DELETE FROM recipes WHERE id = %s', (recipe_id,))
        conn.commit()
        
        return jsonify({'success': True, 'message': f'Recipe "{recipe["title"]}" deleted successfully!'})
        
    except Exception as e:
        conn.rollback()
        print(f"Error: {e}")
        return jsonify({'success': False, 'message': 'An error occurred. Please try again.'}), 500
    finally:
        cur.close()
        conn.close()

@app.route('/api/recipes/<int:recipe_id>/rate', methods=['POST'])
@login_required
def rate_recipe(recipe_id):
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest' or request.is_json
    
    rating = request.form.get('rating')
    review = request.form.get('review', '').strip()
    
    if not rating or not rating.isdigit() or int(rating) < 1 or int(rating) > 5:
        message = 'Rating must be between 1 and 5.'
        if is_ajax:
            return jsonify({'success': False, 'message': message})
        flash(message, 'error')
        return redirect(url_for('recipes'))
    
    rating = int(rating)
    
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    
    # Check if recipe exists and is not owned by current user
    cur.execute('SELECT user_id FROM recipes WHERE id = %s', (recipe_id,))
    recipe = cur.fetchone()
    
    if not recipe:
        cur.close()
        conn.close()
        message = 'Recipe not found.'
        if is_ajax:
            return jsonify({'success': False, 'message': message}), 404
        flash(message, 'error')
        return redirect(url_for('recipes'))
    
    if recipe['user_id'] == session['user_id']:
        cur.close()
        conn.close()
        message = 'You cannot rate your own recipe.'
        if is_ajax:
            return jsonify({'success': False, 'message': message})
        flash(message, 'error')
        return redirect(url_for('recipes'))
    
    try:
        # Insert or update rating
        cur.execute('''
            INSERT INTO recipe_ratings (recipe_id, user_id, rating, review)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (recipe_id, user_id) 
            DO UPDATE SET rating = EXCLUDED.rating, 
                         review = EXCLUDED.review,
                         updated_at = CURRENT_TIMESTAMP
        ''', (recipe_id, session['user_id'], rating, review))
        
        conn.commit()
        
        # Get updated average rating
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
        return redirect(url_for('recipes'))
        
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
    
    return redirect(url_for('recipes'))

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
