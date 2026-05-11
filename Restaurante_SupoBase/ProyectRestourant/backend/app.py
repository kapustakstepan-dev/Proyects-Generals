import os
from flask import Flask
from flask_login import LoginManager, UserMixin
from .supabase_client import supabase
from .routes import routes

app = Flask(__name__, 
            template_folder='../frontend/templates', 
            static_folder='../frontend/static')

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-key')

# --- LOGIN MANAGER ---
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'routes.login'

class User(UserMixin):
    def __init__(self, data):
        self.id = data.get('id')
        self.nickname = data.get('nickname')
        self.role = data.get('role', 'user')

@login_manager.user_loader
def load_user(user_id):
    res = supabase.table("users").select("*").eq("id", user_id).execute()
    return User(res.data[0]) if res.data else None

# Register Routes
app.register_blueprint(routes)

if __name__ == '__main__':
    app.run(debug=True)
