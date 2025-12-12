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
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
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
        
    print("Database tables initialized successfully.")
