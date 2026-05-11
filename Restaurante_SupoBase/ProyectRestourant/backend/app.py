import os
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from .supabase_client import supabase
from .auth import register_user, login_user_supabase

app = Flask(__name__, 
            template_folder='../frontend/templates', 
            static_folder='../frontend/static')

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-key-123')

# --- LOGIN MANAGER ---
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

class User(UserMixin):
    def __init__(self, data):
        self.id = data.get('id')
        self.nickname = data.get('nickname')
        self.role = data.get('role', 'user')
        self.email = data.get('email', '')

@login_manager.user_loader
def load_user(user_id):
    try:
        res = supabase.table("users").select("*").eq("id", user_id).execute()
        return User(res.data[0]) if res.data else None
    except:
        return None

# --- ROUTES ---

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        res = login_user_supabase(request.form['username'], request.form['password'])
        if res['success']:
            login_user(User(res['profile']))
            return redirect(url_for('menu'))
        flash("Invalid credentials")
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        res = register_user(request.form['email'], request.form['password'])
        if res['success']:
            flash("Check email to confirm!")
            return redirect(url_for('login'))
        flash(res['error'])
    return render_template('register.html')

@app.route('/logout')
@login_required
def logout():
    supabase.auth.sign_out()
    logout_user()
    return redirect(url_for('login'))

@app.route('/menu')
def menu():
    res = supabase.table("menu").select("*").eq("active", True).execute()
    return render_template('menu.html', menu_items=res.data)

@app.route('/position/<int:position_id>', methods=['GET', 'POST'])
def position(position_id):
    res = supabase.table("menu").select("*").eq("id", position_id).execute()
    if not res.data: return render_template('404.html'), 404
    item = res.data[0]
    
    if request.method == 'POST':
        qty = int(request.form.get('quantity', 1))
        if 'basket' not in session: session['basket'] = {}
        # Store item name for the template's simple display
        session['basket'][str(item['id'])] = session['basket'].get(str(item['id']), 0) + qty
        session.modified = True
        return redirect(url_for('menu'))
        
    return render_template('position.html', position=item)

@app.route('/create_order', methods=['GET', 'POST'])
@login_required
def create_order():
    basket = session.get('basket', {})
    if not basket: return redirect(url_for('menu'))
    
    # Calculate Total & Prepare items for receipt
    items_for_json = []
    total = 0
    # Map for the template's display (Name -> Qty)
    display_basket = {}
    
    for id_str, qty in basket.items():
        res = supabase.table("menu").select("*").eq("id", int(id_str)).execute()
        if res.data:
            it = res.data[0]
            total += it['price'] * qty
            items_for_json.append({"name": it['name'], "qty": qty, "price": it['price']})
            display_basket[it['name']] = qty

    if request.method == 'POST':
        # Database transaction logic
        order_res = supabase.table("orders").insert({"user_id": current_user.id, "total_price": total}).execute()
        if order_res.data:
            order_id = order_res.data[0]['id']
            # Re-map ids to order_items
            items_data = []
            for id_str, qty in basket.items():
                res = supabase.table("menu").select("price").eq("id", int(id_str)).execute()
                price = res.data[0]['price'] if res.data else 0
                items_data.append({"order_id": order_id, "menu_id": int(id_str), "quantity": qty, "unit_price": price})
            
            supabase.table("order_items").insert(items_data).execute()
            session.pop('basket', None)
            
            return jsonify({
                "success": True, 
                "order_id": str(order_id)[:8], # Short version for display
                "total": total, 
                "items": items_for_json,
                "date": datetime.now().strftime("%Y-%m-%d %H:%M")
            })
            
    return render_template('create_order.html', basket=display_basket, total_price=round(total, 2))

@app.route('/my_orders')
@login_required
def my_orders():
    # Simple list of orders
    res = supabase.table("orders").select("*, order_items(*, menu(*))").eq("user_id", current_user.id).order('order_time', desc=True).execute()
    return render_template('my_orders.html', orders=res.data)

@app.route('/reservation', methods=['GET', 'POST'])
@login_required
def reservation():
    if request.method == 'POST':
        supabase.table("reservations").insert({
            "time_start": request.form['datetime'],
            "type_table": request.form['table_type'],
            "user_id": current_user.id
        }).execute()
        flash("Table reserved!")
        return redirect(url_for('my_reservations'))
    return render_template('reservation.html')

@app.route('/my_reservations')
@login_required
def my_reservations():
    # Fetch both reservations and orders to show history
    res = supabase.table("reservations").select("*").eq("user_id", current_user.id).order('created_at', desc=True).execute()
    orders = supabase.table("orders").select("*").eq("user_id", current_user.id).order('order_time', desc=True).execute()
    return render_template('my_reservations.html', reservations=res.data, orders=orders.data)

@app.route('/admin')
@login_required
def admin():
    if current_user.role != 'admin': return "Access Denied", 403
    menu_items = supabase.table("menu").select("*").execute().data
    all_orders = supabase.table("orders").select("*, users(nickname)").execute().data
    return render_template('admin.html', items=menu_items, orders=all_orders)

if __name__ == '__main__':
    app.run(debug=True)
