"""
Database models and utilities for Forkcast application.
"""

import psycopg2
from psycopg2.extras import RealDictCursor
from contextlib import contextmanager

from .config import Config


@contextmanager
def get_db_connection():
    """
    Context manager for database connections.
    Automatically handles connection cleanup.
    """
    conn = None
    try:
        conn = psycopg2.connect(
            dbname=Config.DB_NAME,
            user=Config.DB_USER,
            password=Config.DB_PASSWORD,
            host=Config.DB_HOST,
            port=Config.DB_PORT
        )
        yield conn
    finally:
        if conn is not None:
            conn.close()


@contextmanager
def get_db_cursor(commit=False):
    """
    Context manager for database cursors with automatic cleanup.
    
    Args:
        commit: If True, commits the transaction after successful execution.
    """
    with get_db_connection() as conn:
        cur = conn.cursor(cursor_factory=RealDictCursor)
        try:
            yield cur
            if commit:
                conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            cur.close()


def init_tables():
    """Initialize database tables."""
    with get_db_cursor(commit=True) as cur:
        # Create users table
        cur.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                username VARCHAR(50) UNIQUE NOT NULL,
                email VARCHAR(100) UNIQUE NOT NULL,
                password_hash VARCHAR(255) NOT NULL,
                full_name VARCHAR(100),
                bio TEXT,
                profile_image VARCHAR(255),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Add profile_image column if it doesn't exist (for existing databases)
        cur.execute('''
            DO $$ 
            BEGIN 
                IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
                               WHERE table_name='users' AND column_name='profile_image') THEN
                    ALTER TABLE users ADD COLUMN profile_image VARCHAR(255);
                END IF;
            END $$;
        ''')
        
        # Create recipes table
        cur.execute('''
            CREATE TABLE IF NOT EXISTS recipes (
                id SERIAL PRIMARY KEY,
                user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
                title VARCHAR(200) NOT NULL,
                description TEXT,
                ingredients TEXT NOT NULL,
                instructions TEXT NOT NULL,
                prep_time INTEGER,
                cook_time INTEGER,
                servings INTEGER,
                calories_per_serving INTEGER,
                category VARCHAR(50),
                cuisine VARCHAR(50),
                difficulty VARCHAR(20),
                tags VARCHAR(500),
                image_url VARCHAR(255),
                is_public BOOLEAN DEFAULT true,
                is_favorite BOOLEAN DEFAULT false,
                forked_from_id INTEGER REFERENCES recipes(id) ON DELETE SET NULL,
                original_author_id INTEGER REFERENCES users(id) ON DELETE SET NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Add fork columns if they don't exist (for existing databases)
        cur.execute('''
            DO $$ 
            BEGIN 
                IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
                               WHERE table_name='recipes' AND column_name='forked_from_id') THEN
                    ALTER TABLE recipes ADD COLUMN forked_from_id INTEGER REFERENCES recipes(id) ON DELETE SET NULL;
                END IF;
                IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
                               WHERE table_name='recipes' AND column_name='original_author_id') THEN
                    ALTER TABLE recipes ADD COLUMN original_author_id INTEGER REFERENCES users(id) ON DELETE SET NULL;
                END IF;
            END $$;
        ''')
        
        # Create recipe ratings table
        cur.execute('''
            CREATE TABLE IF NOT EXISTS recipe_ratings (
                id SERIAL PRIMARY KEY,
                recipe_id INTEGER REFERENCES recipes(id) ON DELETE CASCADE,
                user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
                rating INTEGER CHECK (rating >= 1 AND rating <= 5),
                review TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(recipe_id, user_id)
            )
        ''')
        
        # Create meal_plans table for saving meal plan templates
        cur.execute('''
            CREATE TABLE IF NOT EXISTS meal_plans (
                id SERIAL PRIMARY KEY,
                user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
                name VARCHAR(200) NOT NULL,
                description TEXT,
                week_start_date DATE,
                meals JSONB NOT NULL DEFAULT '{}',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create weekly_calendar_data table for auto-saving calendar meals per week
        cur.execute('''
            CREATE TABLE IF NOT EXISTS weekly_calendar_data (
                id SERIAL PRIMARY KEY,
                user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
                week_start_date DATE NOT NULL,
                meals JSONB NOT NULL DEFAULT '{}',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(user_id, week_start_date)
            )
        ''')
        
        # Create user_nutrition_goals table for calorie/macro tracking
        cur.execute('''
            CREATE TABLE IF NOT EXISTS user_nutrition_goals (
                id SERIAL PRIMARY KEY,
                user_id INTEGER REFERENCES users(id) ON DELETE CASCADE UNIQUE,
                calorie_goal INTEGER DEFAULT 2000,
                protein_goal INTEGER DEFAULT 150,
                carbs_goal INTEGER DEFAULT 200,
                fats_goal INTEGER DEFAULT 67,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create calorie_logs table for tracking daily calorie intake
        cur.execute('''
            CREATE TABLE IF NOT EXISTS calorie_logs (
                id SERIAL PRIMARY KEY,
                user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
                recipe_id INTEGER REFERENCES recipes(id) ON DELETE SET NULL,
                log_date DATE DEFAULT CURRENT_DATE,
                calories INTEGER,
                servings DECIMAL(4,2) DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create notifications table with extended fields for navigation
        cur.execute('''
            CREATE TABLE IF NOT EXISTS notifications (
                id SERIAL PRIMARY KEY,
                user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
                title VARCHAR(255) NOT NULL,
                message TEXT,
                type VARCHAR(50) DEFAULT 'info',
                is_read BOOLEAN DEFAULT false,
                action_url VARCHAR(500),
                action_data JSONB,
                related_id INTEGER,
                from_user_id INTEGER REFERENCES users(id) ON DELETE SET NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Add new columns to notifications if they don't exist
        cur.execute('''
            DO $$ 
            BEGIN 
                IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
                               WHERE table_name='notifications' AND column_name='action_url') THEN
                    ALTER TABLE notifications ADD COLUMN action_url VARCHAR(500);
                END IF;
                IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
                               WHERE table_name='notifications' AND column_name='action_data') THEN
                    ALTER TABLE notifications ADD COLUMN action_data JSONB;
                END IF;
                IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
                               WHERE table_name='notifications' AND column_name='related_id') THEN
                    ALTER TABLE notifications ADD COLUMN related_id INTEGER;
                END IF;
                IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
                               WHERE table_name='notifications' AND column_name='from_user_id') THEN
                    ALTER TABLE notifications ADD COLUMN from_user_id INTEGER REFERENCES users(id) ON DELETE SET NULL;
                END IF;
            END $$;
        ''')
        
        # Create meal_reminder_settings table for user notification preferences
        cur.execute('''
            CREATE TABLE IF NOT EXISTS meal_reminder_settings (
                id SERIAL PRIMARY KEY,
                user_id INTEGER REFERENCES users(id) ON DELETE CASCADE UNIQUE,
                reminders_enabled BOOLEAN DEFAULT true,
                breakfast_time TIME DEFAULT '08:00',
                lunch_time TIME DEFAULT '12:00',
                dinner_time TIME DEFAULT '18:00',
                snack_time TIME DEFAULT '15:00',
                breakfast_reminder_minutes INTEGER DEFAULT 30,
                lunch_reminder_minutes INTEGER DEFAULT 30,
                dinner_reminder_minutes INTEGER DEFAULT 30,
                snack_reminder_minutes INTEGER DEFAULT 30,
                notify_weekly_plan BOOLEAN DEFAULT true,
                notify_shopping_list BOOLEAN DEFAULT true,
                notify_new_recipes BOOLEAN DEFAULT true,
                notify_calorie_goal BOOLEAN DEFAULT true,
                sound_enabled BOOLEAN DEFAULT true,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create shopping_list table
        cur.execute('''
            CREATE TABLE IF NOT EXISTS shopping_list (
                id SERIAL PRIMARY KEY,
                user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
                item_name VARCHAR(255) NOT NULL,
                quantity VARCHAR(100),
                unit VARCHAR(50),
                category VARCHAR(100),
                is_checked BOOLEAN DEFAULT false,
                source VARCHAR(50) DEFAULT 'manual',
                recipe_id INTEGER REFERENCES recipes(id) ON DELETE SET NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Add source and recipe_id columns if they don't exist (for existing databases)
        cur.execute('''
            DO $$ 
            BEGIN 
                IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
                               WHERE table_name='shopping_list' AND column_name='source') THEN
                    ALTER TABLE shopping_list ADD COLUMN source VARCHAR(50) DEFAULT 'manual';
                END IF;
                IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
                               WHERE table_name='shopping_list' AND column_name='recipe_id') THEN
                    ALTER TABLE shopping_list ADD COLUMN recipe_id INTEGER REFERENCES recipes(id) ON DELETE SET NULL;
                END IF;
            END $$;
        ''')
        
    print("Database tables initialized successfully.")
