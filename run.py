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
    # Initialize database tables
    init_tables()
    
    # Run development server
    app.run(debug=True, port=1405)
