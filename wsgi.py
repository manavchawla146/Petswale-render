"""
WSGI entry point for Render deployment
"""

import os
from PetPocket import create_app
from PetPocket.config import ProductionConfig

# Create the Flask app with production configuration
app = create_app(ProductionConfig)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
