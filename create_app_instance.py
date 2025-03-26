# wsgi.py

import os
from src.app import create_app

# Create the application instance
app = create_app()

if __name__ == "__main__":
    # Ensure templates directory exists
    if not os.path.exists('templates'):
        os.makedirs('templates')
    app.run()