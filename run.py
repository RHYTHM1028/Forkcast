#!/usr/bin/env python3
"""
Forkcast Application Entry Point

This script runs the Flask development server.
For production, use a WSGI server like Gunicorn.
"""

from forkcast import create_app
from forkcast.models import init_tables

app = create_app()

if __name__ == '__main__':
<<<<<<< HEAD
    # Initialize database tables (skip if remote database already set up)
    # init_tables()
    
    # Run production server
    app.run(debug=False, port=3007, host='0.0.0.0')
=======
    # Initialize database tables
    init_tables()
    
    # Run development server
    app.run(debug=True, port=1405)
>>>>>>> Forkcast/feature/meal-reminders
