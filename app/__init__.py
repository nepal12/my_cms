from flask import Flask
from dotenv import load_dotenv
from app.extensions import db, migrate, login_manager
from app.utils import user_has_capability
import datetime

load_dotenv()

def create_app():
    app = Flask(__name__)
    app.config['Debug'] = True
    app.config.from_object('app.config.Config')

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message_category = 'info'

    app.context_processor(lambda: dict(user_has_capability=user_has_capability))
    
    @app.context_processor  # This decorator is essential
    def inject_current_year():
        return {'current_year': datetime.datetime.now().year}  # Return a dictionary

    from app.models import User, Post
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    from app.views.auth import auth_bp
    app.register_blueprint(auth_bp)
    from app.views.main import main_bp
    app.register_blueprint(main_bp)
    from app.views.post import post_bp
    app.register_blueprint(post_bp)
    from app.views.admin import admin_bp
    app.register_blueprint(admin_bp)

    return app