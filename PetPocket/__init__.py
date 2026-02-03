from flask import Flask, request, jsonify, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user
from flask_migrate import Migrate
from flask_mail import Mail
from flask_wtf.csrf import CSRFProtect, CSRFError
import os
import razorpay

db = SQLAlchemy()
mail = Mail()
csrf = CSRFProtect()
razorpay_client = None


def create_app(config_class):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # ---- HARD FAIL IF DB NOT SET (PROD SAFETY) ----
    if not app.config.get("SQLALCHEMY_DATABASE_URI"):
        raise RuntimeError("DATABASE IS NOT CONFIGURED")

    # ---- INIT EXTENSIONS ----
    db.init_app(app)
    mail.init_app(app)
    csrf.init_app(app)
    Migrate(app, db)

    login_manager = LoginManager()
    login_manager.login_view = "auth.signin"
    login_manager.init_app(app)

    # ---- LOGIN ----
    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    @login_manager.unauthorized_handler
    def unauthorized():
        if request.is_json:
            return jsonify(success=False, message="Login required"), 401
        return redirect(url_for("auth.login"))

    # ---- RAZORPAY ----
    global razorpay_client
    razorpay_client = razorpay.Client(
        auth=(
            app.config["RAZORPAY_KEY_ID"],
            app.config["RAZORPAY_KEY_SECRET"],
        )
    )

    # ---- BLUEPRINTS ----
    from .routes import main
    from .auth import auth
    from .admin.analytics import admin_analytics
    from .admin import init_admin

    app.register_blueprint(main)
    app.register_blueprint(auth, url_prefix="/auth")
    app.register_blueprint(admin_analytics, url_prefix="/admin")
    init_admin(app, db)

    # ---- CONTEXT ----
    @app.context_processor
    def inject_cart_count():
        from .models import CartItem
        from sqlalchemy import func

        if current_user.is_authenticated:
            count = (
                db.session.query(func.sum(CartItem.quantity))
                .filter_by(user_id=current_user.id)
                .scalar()
                or 0
            )
        else:
            count = 0
        return dict(cart_count=int(count))

    # ---- HEALTH CHECK (RENDER) ----
    @app.route("/health")
    def health():
        return "ok", 200

    # ---- SECURITY HEADERS ----
    @app.after_request
    def security_headers(response):
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "SAMEORIGIN"
        response.headers["Cross-Origin-Opener-Policy"] = "same-origin-allow-popups"
        return response

    # ---- ERRORS ----
    @app.errorhandler(CSRFError)
    def csrf_error(e):
        return "CSRF error", 400

    @app.errorhandler(500)
    def server_error(e):
        db.session.rollback()
        return "Internal Server Error", 500

    return app
