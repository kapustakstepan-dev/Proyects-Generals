from flask import Blueprint, request, jsonify, render_template, redirect, url_for, session, flash
from flask_login import login_user, logout_user, login_required, current_user
from .supabase_client import supabase
from .auth import register_user, login_user_supabase
from datetime import datetime

routes = Blueprint('routes', __name__)

# --- AUTH ---
@routes.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        res = register_user(request.form['email'], request.form['password'])
        if res['success']:
            flash("Check email to confirm!")
            return redirect(url_for('routes.login'))
        flash(res['error'])
    return render_template('register.html')

@routes.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        res = login_user_supabase(request.form['username'], request.form['password'])
        if res['success']:
            # Minimal user class for flask-login
            from .app import User
            login_user(User(res['profile']))
            return redirect(url_for('routes.menu_view'))
        flash("Login failed")
    return render_template('login.html')

@routes.route('/logout')
@login_required
def logout():
    supabase.auth.sign_out()
    logout_user()
    return redirect(url_for('routes.login'))

# --- MENU ---
@routes.route('/menu')
def menu_view():
    res = supabase.table("menu").select("*").eq("active", True).execute()
    return render_template('menu.html', menu_items=res.data)

# --- ORDERS ---
@routes.route('/create_order', methods=['GET', 'POST'])
@login_required
def create_order():
    basket = session.get('basket', {})
    if request.method == 'POST':
        # Simple Order Logic
        total = 0
        items_data = []
        for id_str, qty in basket.items():
            item = supabase.table("menu").select("*").eq("id", int(id_str)).execute().data[0]
            total += item['price'] * qty
            items_data.append({"menu_id": item['id'], "quantity": qty, "unit_price": item['price']})
        
        order = supabase.table("orders").insert({"user_id": current_user.id, "total_price": total}).execute()
        if order.data:
            order_id = order.data[0]['id']
            for i in items_data: i['order_id'] = order_id
            supabase.table("order_items").insert(items_data).execute()
            session.pop('basket', None)
            return jsonify({"success": True, "order_id": order_id})
            
    return render_template('create_order.html', basket=basket)

# --- RESERVATIONS ---
@routes.route('/reservation', methods=['GET', 'POST'])
@login_required
def reservation():
    if request.method == 'POST':
        supabase.table("reservations").insert({
            "time_start": request.form['datetime'],
            "type_table": request.form['table_type'],
            "user_id": current_user.id
        }).execute()
        flash("Reserved!")
        return redirect(url_for('routes.my_reservations'))
    return render_template('reservation.html')

@routes.route('/my_reservations')
@login_required
def my_reservations():
    res = supabase.table("reservations").select("*").eq("user_id", current_user.id).execute()
    return render_template('my_reservations.html', reservations=res.data)

# --- ADMIN ---
@routes.route('/admin')
@login_required
def admin():
    if current_user.role != 'admin': return "Access Denied", 403
    menu = supabase.table("menu").select("*").execute().data
    orders = supabase.table("orders").select("*, users(nickname)").execute().data
    return render_template('admin.html', items=menu, orders=orders)
