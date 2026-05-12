import os
import logging
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from supabase_client import supabase
from auth import register_user, login_user_supabase

# --- LOGGING SETUP ---
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')

app = Flask(__name__, 
            template_folder='../frontend/templates', 
            static_folder='../frontend/static')

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'default-pro-key-99')

# --- LOGIN MANAGER ---
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

class User(UserMixin):
    def __init__(self, data):
        self.id = data.get('id')
        self.nickname = data.get('nickname')
        self.role = data.get('role', 'user')

@login_manager.user_loader
def load_user(user_id):
    try:
        res = supabase.table("users").select("*").eq("id", user_id).execute()
        if res.data:
            return User(res.data[0])
        return None
    except Exception as e:
        logging.error(f"Error loading user {user_id}: {e}")
        return None

# --- CORE ROUTES ---

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/menu')
def menu():
    try:
        res = supabase.table("menu").select("*").eq("active", True).execute()
        logging.info(f"Fetched {len(res.data)} menu items from Supabase.")
        return render_template('menu.html', menu_items=res.data)
    except Exception as e:
        logging.error(f"Failed to fetch menu: {e}")
        return render_template('menu.html', menu_items=[], error="Database connection error.")

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        res = login_user_supabase(request.form['username'], request.form['password'])
        if res['success']:
            login_user(User(res['profile']))
            logging.info(f"User {current_user.id} logged in successfully.")
            return redirect(url_for('menu'))
        flash("Invalid credentials.")
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        res = register_user(request.form['email'], request.form['password'])
        if res['success']:
            flash("Registered! Please check your email to confirm.")
            return redirect(url_for('login'))
        flash(res['error'])
    return render_template('register.html')

@app.route('/logout')
@login_required
def logout():
    uid = current_user.id
    # supabase.auth.sign_out()
    logout_user()
    logging.info(f"User {uid} logged out.")
    return redirect(url_for('login'))

@app.route('/position/<int:position_id>', methods=['GET', 'POST'])
def position(position_id):
    res = supabase.table("menu").select("*").eq("id", position_id).execute()
    if not res.data: return render_template('404.html'), 404
    item = res.data[0]
    
    if request.method == 'POST':
        try:
            qty = int(request.form.get('quantity', 1))
            if qty < 1: raise ValueError("Quantity must be positive.")
            if 'basket' not in session: session['basket'] = {}
            session['basket'][str(item['id'])] = session['basket'].get(str(item['id']), 0) + qty
            session.modified = True
            return redirect(url_for('menu'))
        except Exception as e:
            flash(str(e))
        
    return render_template('position.html', position=item)

@app.route('/create_order', methods=['GET', 'POST'])
@login_required
def create_order():
    basket = session.get('basket', {})
    if not basket: return redirect(url_for('menu'))
    
    # Recalculate everything from DB (Backend-only truth)
    items_to_display = []
    items_to_insert = []
    total_price = 0
    
    try:
        for mid_str, qty in basket.items():
            res = supabase.table("menu").select("*").eq("id", int(mid_str)).execute()
            if res.data:
                it = res.data[0]
                price = it['price']
                total_price += price * qty
                items_to_display.append({"name": it['name'], "qty": qty, "price": price})
                items_to_insert.append({"menu_id": it['id'], "quantity": qty, "unit_price": price})

        if request.method == 'POST':
            order_res = supabase.table("orders").insert({
                "user_id": current_user.id, 
                "total_price": total_price
            }).execute()
            
            if order_res.data:
                oid = order_res.data[0]['id']
                for i in items_to_insert: i['order_id'] = oid
                supabase.table("order_items").insert(items_to_insert).execute()
                
                logging.info(f"Order {oid} created by user {current_user.id}. Total: {total_price}")
                session.pop('basket', None)
                return jsonify({"success": True, "order_id": str(oid)[:8]})
                
    except Exception as e:
        logging.error(f"Checkout error: {e}")
        return jsonify({"success": False, "error": "Internal server error."}), 500
            
    return render_template('create_order.html', basket_items=items_to_display, total_price=round(total_price, 2))

@app.route('/my_orders')
@login_required
def my_orders():
    res = supabase.table("orders").select("*, order_items(*, menu(*))").eq("user_id", current_user.id).order('order_time', desc=True).execute()
    return render_template('my_orders.html', orders=res.data)

@app.route('/reservation', methods=['GET', 'POST'])
@login_required
def reservation():
    if request.method == 'POST':
        try:
            supabase.table("reservations").insert({
                "time_start": request.form['datetime'],
                "type_table": request.form['table_type'],
                "user_id": current_user.id
            }).execute()
            logging.info(f"Reservation made by user {current_user.id}")
            return redirect(url_for('my_reservations'))
        except Exception as e:
            logging.error(f"Reservation error: {e}")
            flash("Failed to create reservation.")
            
    return render_template('reservation.html')

@app.route('/my_reservations')
@login_required
def my_reservations():
    res = supabase.table("reservations").select("*").eq("user_id", current_user.id).order('created_at', desc=True).execute()
    return render_template('my_reservations.html', reservations=res.data)

@app.route('/admin')
@login_required
def admin():
    if current_user.role != 'admin': return "Forbidden", 403
    menu_items = supabase.table("menu").select("*").execute().data
    orders = supabase.table("orders").select("*, users(nickname)").execute().data
    return render_template('admin.html', items=menu_items, orders=orders)

if __name__ == '__main__':
    app.run(debug=True)
