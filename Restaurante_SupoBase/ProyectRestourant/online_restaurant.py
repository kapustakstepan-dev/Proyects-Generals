import os
import re
import logging
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from flask_login import LoginManager, login_user, logout_user, login_required, current_user, UserMixin
from flask_mail import Mail, Message
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from supabase import create_client, Client
from dotenv import load_dotenv

# --- INITIALIZATION ---
load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'pro-supabase-backend-99')

# Logging Setup
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Rate Limiting (In-memory for serverless instance protection)
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["100 per day", "30 per hour"],
    storage_uri="memory://",
)

# Supabase Client
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Flask-Mail
app.config.update(
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT=587,
    MAIL_USE_TLS=True,
    MAIL_USERNAME=os.getenv('MAIL_USERNAME'),
    MAIL_PASSWORD=os.getenv('MAIL_PASSWORD'),
    MAIL_DEFAULT_SENDER=os.getenv('MAIL_DEFAULT_SENDER', os.getenv('MAIL_USERNAME'))
)
mail = Mail(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# --- HELPERS ---
class DBObject:
    def __init__(self, data):
        if data:
            for key, value in data.items():
                setattr(self, key, value)
    def __getattr__(self, name): return None

class User(UserMixin, DBObject):
    """Modern User class using UUID. Email is pulled from Auth if missing in Profile."""
    def __init__(self, data, email=None):
        super().__init__(data)
        self.id = data.get('id')
        self.nickname = data.get('nickname')
        self.role = data.get('role', 'user')
        self.email = email or data.get('email')

def parse_db_date(date_str):
    if not date_str: return None
    try: return datetime.fromisoformat(date_str.replace('Z', '+00:00'))
    except: return datetime.now()

def validate_email(email):
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)

@login_manager.user_loader
def load_user(user_id):
    try:
        # Fetch profile from public.users
        res = supabase.table("users").select("*").eq("id", user_id).execute()
        if res.data:
            # Note: Email isn't in public.users, but we have it in the session if needed.
            # For general Flask-Login use, ID and Role are sufficient.
            return User(res.data[0])
        return None
    except Exception as e:
        logging.error(f"User loading failed: {e}")
        return None

# --- CORE ROUTES ---
@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/menu')
def menu_view():
    try:
        res = supabase.table("menu").select("*").eq("active", True).execute()
        items = [DBObject(item) for item in res.data]
        return render_template('menu.html', menu_items=items)
    except Exception as e:
        logging.error(f"Menu fetch error: {e}")
        return render_template('menu.html', menu_items=[])

@app.route('/register', methods=['GET', 'POST'])
@limiter.limit("5 per minute")
def register():
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '').strip()
        
        if not email or not password:
            flash("All fields are required.")
            return redirect(url_for('register'))
        
        if not validate_email(email):
            flash("Invalid email format.")
            return redirect(url_for('register'))

        try:
            # Trigger 'handle_new_user' creates public.users profile automatically
            res = supabase.auth.sign_up({"email": email, "password": password})
            if res.user:
                flash("Registered! Check your email to verify account.")
                return redirect(url_for('login'))
        except Exception as e:
            logging.error(f"Registration error: {e}")
            flash(f"Error: {str(e)}")
            
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
@limiter.limit("10 per minute")
def login():
    if request.method == 'POST':
        email = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()
        
        try:
            res = supabase.auth.sign_in_with_password({"email": email, "password": password})
            if res.user:
                # Fetch profile from public.users (simplified schema)
                profile = supabase.table("users").select("*").eq("id", res.user.id).execute()
                if profile.data:
                    user = User(profile.data[0], email=res.user.email)
                    login_user(user)
                    logging.info(f"Login success: {user.id}")
                    return redirect(url_for('menu'))
            flash("Invalid credentials.")
        except Exception as e:
            logging.error(f"Login failed: {e}")
            flash("Login error.")
            
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    supabase.auth.sign_out()
    logout_user()
    return redirect(url_for('login'))

@app.route('/position/<int:position_id>', methods=['GET', 'POST'])
def position(position_id):
    res = supabase.table("menu").select("*").eq("id", position_id).execute()
    if not res.data: return render_template('404.html'), 404
    
    pos = DBObject(res.data[0])
    if request.method == 'POST':
        try:
            qty = int(request.form.get('quantity', 1))
            if qty < 1 or qty > 20: raise ValueError()
            if 'basket' not in session: session['basket'] = {}
            session['basket'][str(pos.id)] = session['basket'].get(str(pos.id), 0) + qty
            session.modified = True
            return redirect(url_for('position', position_id=position_id))
        except:
            flash("Quantity limit (20) exceeded.")

    return render_template("position.html", position=pos)

@app.route('/create_order', methods=['GET', 'POST'])
@login_required
def create_order():
    basket = session.get('basket', {})
    if not basket: return redirect(url_for('menu'))
    
    try:
        basket_items = []
        total_price = 0
        for item_id, quantity in basket.items():
            res = supabase.table("menu").select("*").eq("id", int(item_id)).execute()
            if res.data:
                item = DBObject(res.data[0])
                basket_items.append({'item': item, 'quantity': quantity})
                total_price += item.price * quantity

        if request.method == 'POST':
            # Create Order + Items (UUID generated by DB default)
            order_res = supabase.table("orders").insert({
                "user_id": current_user.id,
                "total_price": total_price,
                "state": 'confirmed'
            }).execute()
            
            if order_res.data:
                order_id = order_res.data[0]['id']
                items_insert = [{"order_id": order_id, "menu_id": bi['item'].id, "quantity": bi['quantity'], "unit_price": bi['item'].price} for bi in basket_items]
                supabase.table("order_items").insert(items_insert).execute()
                
                session.pop('basket', None)
                logging.info(f"Order {order_id} created by {current_user.id}")
                return jsonify({"success": True, "order_id": order_id, "total": total_price})

        return render_template('create_order.html', basket=basket, total_price=total_price)
    except Exception as e:
        logging.error(f"Order error: {e}")
        return jsonify({"success": False}), 500

@app.route('/reservation', methods=['GET', 'POST'])
@login_required
@limiter.limit("3 per minute")
def reservation():
    if request.method == 'POST':
        try:
            dt_str = request.form.get('datetime', '')
            if not dt_str: return redirect(url_for('reservation'))
            
            time_start = datetime.strptime(dt_str, "%Y-%m-%dT%H:%M")
            if time_start < datetime.now():
                flash("Cannot reserve in the past.")
                return redirect(url_for('reservation'))

            supabase.table("reservations").insert({
                "time_start": time_start.isoformat(),
                "type_table": request.form.get('table_type', 'standard'),
                "user_id": current_user.id
            }).execute()
            flash("Reservation confirmed!")
            return redirect(url_for('my_reservations'))
        except Exception as e:
            logging.error(f"Res error: {e}")
            flash("Reservation error.")
        
    return render_template('reservation.html')

@app.route('/my_reservations')
@login_required
def my_reservations():
    try:
        reservations = [DBObject(r) for r in supabase.table("reservations").select("*").eq("user_id", current_user.id).execute().data]
        for r in reservations: r.time_start = parse_db_date(r.time_start)
        
        orders = [DBObject(o) for o in supabase.table("orders").select("*").eq("user_id", current_user.id).execute().data]
        for o in orders: o.order_time = parse_db_date(o.order_time)
        
        return render_template('my_reservations.html', reservations=reservations, orders=orders)
    except Exception as e:
        logging.error(f"My Reservations fail: {e}")
        return render_template('404.html'), 404

# --- ADMIN DASHBOARD ---
@app.route('/admin')
@login_required
def admin():
    if current_user.role != 'admin': return render_template('403.html'), 403
    tab = request.args.get('tab', 'menu')
    
    try:
        # Dashboard Analytics
        orders_raw = supabase.table("orders").select("total_price").execute().data
        total_sales = sum(o['total_price'] for o in orders_raw) if orders_raw else 0
        
        items = [DBObject(i) for i in supabase.table("menu").select("*").order("id", desc=True).execute().data]
        # Admin can see nicknames through the users relation (Supabase Join)
        orders = [DBObject(o) for o in supabase.table("orders").select("*, users(nickname)").order("order_time", desc=True).execute().data]
        for o in orders: o.order_time = parse_db_date(o.order_time)
        
        res_list = [DBObject(r) for r in supabase.table("reservations").select("*, users(nickname)").order("time_start", desc=True).execute().data]
        for r in res_list: r.time_start = parse_db_date(r.time_start)
        
        users_list = [DBObject(u) for u in supabase.table("users").select("*").order("created_at", desc=False).execute().data]
        
        return render_template('admin.html', items=items, orders=orders, reservations=res_list, users=users_list, 
                               active_tab=tab, stats={'sales': total_sales, 'count': len(orders_raw)})
    except Exception as e:
        logging.error(f"Admin Error: {e}")
        return render_template('500.html'), 500

@app.route('/admin/menu/add', methods=['POST'])
@login_required
def admin_menu_add():
    if current_user.role != 'admin': return redirect(url_for('home'))
    try:
        supabase.table("menu").insert({
            "name": request.form.get('name', '').strip(),
            "price": float(request.form.get('price', 0)),
            "description": request.form.get('description', ''),
            "category": request.form.get('category', 'burgers')
        }).execute()
        flash("Menu item added.")
    except Exception as e:
        logging.error(f"Add Menu fail: {e}")
        flash("Error adding item.")
    return redirect(url_for('admin', tab='menu'))

@app.route('/admin/order/status/<string:id>', methods=['POST'])
@login_required
def admin_order_status(id):
    if current_user.role != 'admin': return redirect(url_for('home'))
    status = request.form.get('status')
    if status in ['pending', 'confirmed', 'preparing', 'ready', 'delivered', 'cancelled']:
        supabase.table("orders").update({"state": status}).eq("id", id).execute()
    return redirect(url_for('admin', tab='orders'))

# --- SYSTEM ERRORS ---
@app.errorhandler(404)
def error_404(e): return render_template('404.html'), 404

@app.errorhandler(403)
def error_403(e): return render_template('403.html'), 403

@app.errorhandler(500)
def error_500(e): return render_template('500.html'), 500

# Vercel Runtime Export
if __name__ == '__main__':
    app.run(debug=True)
