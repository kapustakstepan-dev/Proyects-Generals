import os
from flask import Flask, render_template
from flask_login import LoginManager, UserMixin
from supabase import create_client
from dotenv import load_dotenv

# Load Blueprints
from .routes.auth import auth_bp
from .routes.menu import menu_bp
from .routes.orders import orders_bp

load_dotenv()

def create_app():
    # Adjusted paths for project structure
    app = Flask(__name__, 
                template_folder='../../frontend/templates', 
                static_folder='../../frontend/static')
    
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'default-pro-key')

    # Shared Supabase for user loading
    supabase = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    class User(UserMixin):
        def __init__(self, data):
            self.id = data.get('id')
            self.nickname = data.get('nickname')
            self.role = data.get('role', 'user')

    @login_manager.user_loader
    def load_user(user_id):
        res = supabase.table("users").select("*").eq("id", user_id).execute()
        return User(res.data[0]) if res.data else None

    # Register Blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(menu_bp)
    app.register_blueprint(orders_bp)

    @app.route('/')
    def index():
        return render_template('home.html')

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html'), 404

    return app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
