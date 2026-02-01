from PetPocket import create_app, db
from PetPocket.config import DevelopmentConfig
import os

# Create app context with development config
app = create_app(DevelopmentConfig)

# Check database connection
with app.app_context():
    try:
        # Test database connection
        from PetPocket.models import User
        user_count = User.query.count()
        print(f"✅ Connected to instance/petpocket.db successfully!")
        print(f"📊 Total users in database: {user_count}")
        
        # Check for admin users
        admin_users = User.query.filter_by(is_admin=True).count()
        print(f"👤 Admin users in database: {admin_users}")
        
        if admin_users == 0:
            print("⚠️  No admin users found. You may need admin access for the admin panel.")
        
    except Exception as e:
        print(f"❌ Error connecting to database: {e}")
        print("Make sure instance/petpocket.db exists and has the required tables")

if __name__ == "__main__":
    # Use development config for local running
    app.run(host="127.0.0.1", port=5000, debug=True)
