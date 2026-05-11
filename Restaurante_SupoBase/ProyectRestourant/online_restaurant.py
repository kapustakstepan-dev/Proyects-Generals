import os
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from flask_login import LoginManager, login_user, logout_user, login_required, current_user, UserMixin
import re
from flask_mail import Mail, Message
from supabase import create_client, Client
from dotenv import load_dotenv

# Initialize Environment
load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'secret-key')

# Supabase Client
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Flask-Mail Config
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_USERNAME')

mail = Mail(app)

# Login Manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# --- HELPER CLASSES FOR TEMPLATE COMPATIBILITY ---
class DBObject:
    """Wraps dictionary data to allow dot notation access (item.name)"""
    def __init__(self, data):
        if data:
            for key, value in data.items():
                setattr(self, key, value)
    
    def __getattr__(self, name):
        return None

class User(UserMixin, DBObject):
    """User class for Flask-Login compatibility using UUID"""
    def __init__(self, data):
        super().__init__(data)
        self.id = data.get('id') # UUID string
        self.nickname = data.get('nickname')
        self.role = data.get('role', 'user')
        self.email = data.get('email')

@login_manager.user_loader
def load_user(user_id):
    try:
        # Check in public.users table
        res = supabase.table("users").select("*").eq("id", user_id).execute()
        return User(res.data[0]) if res.data else None
    except:
        return None

# --- UTILS ---
def parse_db_date(date_str):
    if not date_str: return None
    try:
        return datetime.fromisoformat(date_str.replace('Z', '+00:00'))
    except Exception:
        return datetime.now()

# --- ROUTES ---
@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/menu', endpoint='menu')
def menu_view():
    try:
        res = supabase.table("menu").select("*").eq("active", True).execute()
        items = [DBObject(item) for item in res.data]
        return render_template('menu.html', menu_items=items)
    except Exception as e:
        print(f"Menu error: {e}")
        return render_template('menu.html', menu_items=[])

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        try:
            # Use Supabase Auth to sign up
            res = supabase.auth.sign_up({
                "email": email,
                "password": password
            })
            
            if res.user:
                flash("Registered successfully! Please check your email for confirmation.")
                return redirect(url_for('login'))
            else:
                flash("Registration failed.")
        except Exception as e:
            flash(f"Error: {str(e)}")
            
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['username'] # Assuming username field is email
        password = request.form['password']
        
        try:
            # Sign in with Supabase Auth
            res = supabase.auth.sign_in_with_password({
                "email": email,
                "password": password
            })
            
            if res.user:
                # Fetch public profile
                profile_res = supabase.table("users").select("*").eq("id", res.user.id).execute()
                if profile_res.data:
                    user = User(profile_res.data[0])
                    login_user(user)
                    flash(f"Welcome, {user.nickname}!")
                    return redirect(url_for('menu'))
            
            flash("Invalid email or password")
        except Exception as e:
            print(f"Login error: {e}")
            flash("An error occurred during login")
            
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    supabase.auth.sign_out()
    logout_user()
    flash("Logged out")
    return redirect(url_for('login'))

@app.route('/position/<int:position_id>', methods=['GET', 'POST'])
def position(position_id):
    res = supabase.table("menu").select("*").eq("id", position_id).execute()
    if not res.data: return "Not found", 404
    
    pos = DBObject(res.data[0])
    if 'basket' not in session: session['basket'] = {}

    if request.method == 'POST':
        num = int(request.form.get('quantity', 1))
        session['basket'][str(pos.id)] = session['basket'].get(str(pos.id), 0) + num
        session.modified = True
        return redirect(url_for('position', position_id=position_id))

    return render_template("position.html", position=pos)

@app.route('/create_order', methods=['GET', 'POST'])
@login_required
def create_order():
    basket = session.get('basket', {})
    if not basket: return redirect(url_for('menu'))
    
    basket_items = []
    total_price = 0
    for item_id, quantity in basket.items():
        res = supabase.table("menu").select("*").eq("id", int(item_id)).execute()
        if res.data:
            item = DBObject(res.data[0])
            basket_items.append({'item': item, 'quantity': quantity})
            total_price += item.price * quantity

    if request.method == 'POST':
        # 1. Create Order entry
        res_order = supabase.table("orders").insert({
            "user_id": current_user.id,
            "total_price": total_price,
            "state": 'confirmed'
        }).execute()
        
        if res_order.data:
            order_id = res_order.data[0]['id']
            
            # 2. Insert Order Items
            order_items_data = []
            for bi in basket_items:
                order_items_data.append({
                    "order_id": order_id,
                    "menu_id": bi['item'].id,
                    "quantity": bi['quantity'],
                    "unit_price": bi['item'].price
                })
            
            supabase.table("order_items").insert(order_items_data).execute()
            
            session.pop('basket', None)
            
            return jsonify({
                "success": True,
                "order_id": order_id,
                "total": total_price,
                "items": [{ "name": bi['item'].name, "qty": bi['quantity'], "price": bi['item'].price } for bi in basket_items],
                "date": datetime.now().strftime("%Y-%m-%d %H:%M")
            })

    return render_template('create_order.html', basket=basket, total_price=total_price)

@app.route('/my_orders')
def my_orders():
    basket = session.get('basket', {})
    items = []
    for id_str, quantity in basket.items():
        res = supabase.table("menu").select("*").eq("id", int(id_str)).execute()
        if res.data:
            items.append({"item": DBObject(res.data[0]), "quantity": quantity})
    return render_template("my_orders.html", items=items)

@app.route('/reservation', methods=['GET', 'POST'])
@login_required
def reservation():
    if request.method == 'POST':
        time_start = datetime.strptime(request.form['datetime'], "%Y-%m-%dT%H:%M")
        if time_start < datetime.now():
            flash("Fecha inválida")
            return redirect(url_for('reservation'))

        supabase.table("reservations").insert({
            "time_start": time_start.isoformat(),
            "type_table": request.form['table_type'],
            "user_id": current_user.id,
            "status": 'pending'
        }).execute()

        flash("Reserva creada!")
        return redirect(url_for('my_reservations'))
        
    return render_template('reservation.html')

@app.route('/my_reservations')
@login_required
def my_reservations():
    res_list = [DBObject(r) for r in supabase.table("reservations").select("*").eq("user_id", current_user.id).execute().data]
    for r in res_list: r.time_start = parse_db_date(r.time_start)
    
    order_list = [DBObject(o) for o in supabase.table("orders").select("*").eq("user_id", current_user.id).execute().data]
    for o in order_list: o.order_time = parse_db_date(o.order_time)
    
    return render_template('my_reservations.html', reservations=res_list, orders=order_list)

# --- ADMIN PANEL ---
@app.route('/admin')
@login_required
def admin():
    if current_user.role != 'admin': return redirect(url_for('home'))
    tab = request.args.get('tab', 'menu')
    
    items = [DBObject(i) for i in supabase.table("menu").select("*").order("id", desc=True).execute().data]
    orders = [DBObject(o) for o in supabase.table("orders").select("*").order("order_time", desc=True).execute().data]
    for o in orders: o.order_time = parse_db_date(o.order_time)
    
    reservations = [DBObject(r) for r in supabase.table("reservations").select("*").order("time_start", desc=True).execute().data]
    for r in reservations: r.time_start = parse_db_date(r.time_start)
    
    users = [DBObject(u) for u in supabase.table("users").select("*").order("created_at", desc=False).execute().data]
    
    return render_template('admin.html', items=items, orders=orders, reservations=reservations, users=users, active_tab=tab)

# --- ADMIN CRUD ---
@app.route('/admin/menu/add', methods=['POST'])
@login_required
def admin_menu_add():
    if current_user.role != 'admin': return redirect(url_for('home'))
    supabase.table("menu").insert({
        "name": request.form['name'],
        "price": float(request.form['price']),
        "description": request.form.get('description', ''),
        "weight": request.form.get('weight', '0g'),
        "ingredients": request.form.get('ingredients', 'N/A'),
        "file_name": request.form.get('file_name', 'burger.jpg'),
        "category": request.form.get('category', 'burgers'),
        "active": True
    }).execute()
    flash("Añadido")
    return redirect(url_for('admin', tab='menu'))

@app.route('/admin/order/status/<string:id>', methods=['POST'])
@login_required
def admin_order_status(id):
    if current_user.role != 'admin': return redirect(url_for('home'))
    supabase.table("orders").update({"state": request.form['status']}).eq("id", id).execute()
    return redirect(url_for('admin', tab='orders'))

# --- MAIL ---
@app.route('/send_receipt/<string:order_id>', methods=['POST'])
@login_required
def send_receipt(order_id):
    data = request.get_json()
    email = data.get("email")
    if not email or not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        return jsonify({"success": False, "error": "Invalid email"})

    order_res = supabase.table("orders").select("*").eq("id", order_id).eq("user_id", current_user.id).execute()
    if not order_res.data: return jsonify({"success": False})
    
    order = DBObject(order_res.data[0])
    msg = Message(f"Recibo RetroBite #{order.id}", recipients=[email])
    msg.body = f"Gracias por tu pedido!\nTotal: ${order.total_price:.2f}"
    
    try:
        mail.send(msg)
        return jsonify({"success": True})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

@app.errorhandler(404)
def page_not_found(e): return render_template('404.html'), 404

# Export 'app' for Vercel
if __name__ == '__main__':
    app.run(debug=True)
