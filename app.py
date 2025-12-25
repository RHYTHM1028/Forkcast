#!/usr/bin/env python3
"""
Forkcast Application Entry Point for Pterodactyl Deployment

This is the main entry point that Pterodactyl will execute.
"""

from forkcast import create_app

# Create Flask application instance
app = create_app()

if __name__ == '__main__':
    # Run the application on the Pterodactyl server
    print("🚀 Starting Forkcast")
    print("=" * 50)
    print("🌐 Public URL: http://5.182.206.198:3007")
    print("=" * 50)
    app.run(host='0.0.0.0', port=3007, debug=False)
