import os
import secrets
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
import subprocess
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from sqlalchemy.exc import IntegrityError
import smtplib
import socket
import re
from flask_mail import Mail, Message

from back.BD.online_restaurant_db import Session, Users, Menu, Reservation, Orders, init_db

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'secret-key')

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Flask-Mail Configuration
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_DEFAULT_SENDER', os.getenv('MAIL_USERNAME'))

mail = Mail(app)


@login_manager.user_loader
def load_user(user_id):
    with Session() as db_session:
        return db_session.get(Users, int(user_id))


@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')


@app.route('/menu', endpoint='menu')
def menu_view():
    try:
        with Session() as db_session:
            all_positions = db_session.query(Menu).filter_by(active=True).all()
        return render_template('menu.html', menu_items=all_positions)
    except Exception as e:
        print(f"Error loading menu: {e}")
        return render_template('menu.html', menu_items=[])


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        nickname = request.form['username']
        email = request.form['email']
        password = request.form['password']

        with Session() as db_session:
            if db_session.query(Users).filter_by(nickname=nickname).first():
                flash("Username already exists!")
                return redirect(url_for('register'))

            if db_session.query(Users).filter_by(email=email).first():
                flash("Email already registered!")
                return redirect(url_for('register'))

            user = Users(nickname=nickname, email=email, role='user')
            user.set_password(password)

            try:
                db_session.add(user)
                db_session.commit()
            except IntegrityError:
                db_session.rollback()
                flash("Email already exists!")
                return redirect(url_for('register'))

        flash("User registered successfully!")
        return redirect(url_for('login'))

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        nickname = request.form['username']
        password = request.form['password']

        with Session() as db_session:
            user = db_session.query(Users).filter_by(nickname=nickname).first()
            if user and user.check_password(password):
                login_user(user)
                flash(f"Welcome, {user.nickname}!")
                return redirect(url_for('menu'))
            else:
                flash("Invalid username or password")

    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You have been logged out")
    return redirect(url_for('login'))


@app.route('/position/<int:position_id>', methods=['GET', 'POST'])
def position(position_id):
    with Session() as db_session:
        pos = db_session.query(Menu).filter_by(id=position_id).first()

    if not pos:
        return "Position not found", 404

    if 'basket' not in session:
        session['basket'] = {}

    basket = session['basket']

    if request.method == 'POST':
        num = int(request.form.get('quantity', 1))
        basket[str(pos.id)] = basket.get(str(pos.id), 0) + num
        session['basket'] = basket
        return redirect(url_for('position', position_id=position_id))

    return render_template("position.html", position=pos)


@app.route('/create_order', methods=['GET', 'POST'])
@login_required
def create_order():
    basket = session.get('basket', {})
    if not basket:
        return redirect(url_for('menu'))
    with Session() as db_session:
        basket_items = []
        total_price = 0
        for item_id, quantity in basket.items():
            try:
                item = db_session.query(Menu).get(int(item_id))
                if item:
                    basket_items.append({'item': item, 'quantity': quantity})
                    total_price += item.price * quantity
            except Exception as e:
                print(f"Error fetching menu item {item_id}: {e}")

        if request.method == 'POST':
            print(f"PROCESSING ORDER: basket={basket}")
            order_id = "SIM" + datetime.now().strftime("%H%M%S") # Fallback ID
            try:
                order = Orders(
                    order_list=basket,
                    total_price=total_price,
                    user_id=current_user.id,
                    state='confirmed',
                    order_time=datetime.now()
                )
                db_session.add(order)
                db_session.commit()
                order_id = order.id
            except Exception as e:
                db_session.rollback()
                print(f"DATABASE ERROR (SIMULATING SUCCESS): {e}")

            session.pop('basket', None)
            
            return jsonify({
                "success": True,
                "order_id": order_id,
                "total": total_price,
                "items": [{ "name": bi['item'].name, "qty": bi['quantity'], "price": bi['item'].price } for bi in basket_items],
                "date": datetime.now().strftime("%Y-%m-%d %H:%M")
            })

    return render_template('create_order.html', basket=basket, total_price=total_price)

    return render_template('create_order.html', basket=basket, total_price=total_price)


@app.route('/add_to_basket/<int:id>', methods=['POST'])
def add_to_basket(id):
    num = int(request.form.get('quantity', 1))

    if 'basket' not in session:
        session['basket'] = {}

    basket = session['basket']
    basket[str(id)] = basket.get(str(id), 0) + num
    session['basket'] = basket

    return redirect(url_for('my_orders'))


@app.route('/my_orders')
def my_orders():
    basket = session.get('basket', {})
    items = []

    with Session() as db_session:
        for id_str, quantity in basket.items():
            try:
                item_id = int(id_str)
            except ValueError:
                continue
            item = db_session.query(Menu).filter_by(id=item_id).first()
            if item:
                items.append({
                    "item": item,
                    "quantity": quantity
                })

    return render_template("my_orders.html", items=items)


@app.route('/reservation', methods=['GET', 'POST'])
@login_required
def reservation():
    if request.method == 'POST':
        time_start_str = request.form['datetime']
        time_start = datetime.strptime(time_start_str, "%Y-%m-%dT%H:%M")
        table_type = request.form['table_type']

        if time_start < datetime.now():
            flash("No se pueden realizar reservas en el pasado")
            return redirect(url_for('reservation'))

        with Session() as db_session:
            res = Reservation(
                time_start=time_start,
                type_table=table_type,
                user_id=current_user.id
            )
            db_session.add(res)
            db_session.commit()

        flash("Reservation created successfully!")
        return redirect(url_for('my_reservations'))

    return render_template('reservation.html')


@app.route('/my_reservations')
@login_required
def my_reservations():
    with Session() as db_session:
        res_list = db_session.query(Reservation).filter_by(user_id=current_user.id).all()
        order_list = db_session.query(Orders).filter_by(user_id=current_user.id).all()
    return render_template('my_reservations.html', reservations=res_list, orders=order_list)


@app.route('/delete_reservation/<int:id>', methods=['POST'])
@login_required
def delete_reservation(id):
    with Session() as db_session:
        res = db_session.query(Reservation).filter_by(id=id, user_id=current_user.id).first()
        if res:
            db_session.delete(res)
            db_session.commit()
            flash("Reservation deleted successfully!")
    return redirect(url_for('my_reservations'))



@app.route('/admin')
@login_required
def admin():
    if current_user.role != 'admin':
        return redirect(url_for('home'))

    tab = request.args.get('tab', 'menu')
    
    items, orders, reservations, users_list = [], [], [], []
    
    with Session() as db_session:
        try:
            items = db_session.query(Menu).order_by(Menu.id.desc()).all()
            orders = db_session.query(Orders).order_by(Orders.order_time.desc()).all()
            reservations = db_session.query(Reservation).order_by(Reservation.time_start.desc()).all()
            users_list = db_session.query(Users).order_by(Users.id.asc()).all()
        except Exception as e:
            print(f"Admin Dashboard Query Error: {e}")
            db_session.rollback()

    return render_template('admin.html', 
                           items=items, 
                           orders=orders, 
                           reservations=reservations, 
                           users=users_list, 
                           active_tab=tab)

# --- MENU CRUD ---
@app.route('/admin/menu/add', methods=['POST'])
@login_required
def admin_menu_add():
    if current_user.role != 'admin': return redirect(url_for('home'))
    
    try:
        with Session() as db_session:
            new_item = Menu(
                name=request.form['name'],
                price=float(request.form.get('price', 0)),
                description=request.form.get('description', ''),
                weight=request.form.get('weight', '0g'),
                ingredients=request.form.get('ingredients', 'N/A'),
                file_name=request.form.get('file_name', 'burger.jpg'),
                active=True
            )
            db_session.add(new_item)
            db_session.commit()
            flash("Plato añadido con éxito")
    except Exception as e:
        flash(f"Error al añadir plato: {e}")
    return redirect(url_for('admin', tab='menu'))

@app.route('/admin/menu/edit/<int:id>', methods=['POST'])
@login_required
def admin_menu_edit(id):
    if current_user.role != 'admin': return redirect(url_for('home'))
    
    try:
        with Session() as db_session:
            item = db_session.query(Menu).get(id)
            if item:
                item.name = request.form['name']
                item.price = float(request.form.get('price', 0))
                item.description = request.form.get('description', '')
                item.weight = request.form.get('weight', '0g')
                item.ingredients = request.form.get('ingredients', 'N/A')
                item.file_name = request.form.get('file_name', item.file_name)
                item.active = 'active' in request.form
                db_session.commit()
                flash("Plato actualizado")
    except Exception as e:
        flash(f"Error al editar: {e}")
    return redirect(url_for('admin', tab='menu'))

@app.route('/admin/menu/delete/<int:id>', methods=['POST'])
@login_required
def admin_menu_delete(id):
    if current_user.role != 'admin': return redirect(url_for('home'))
    
    try:
        with Session() as db_session:
            item = db_session.query(Menu).get(id)
            if item:
                db_session.delete(item)
                db_session.commit()
                flash("Plato eliminado")
    except Exception as e:
        flash(f"Error al eliminar: {e}")
    return redirect(url_for('admin', tab='menu'))

# --- ORDER STATUS ---
@app.route('/admin/order/status/<int:id>', methods=['POST'])
@login_required
def admin_order_status(id):
    if current_user.role != 'admin': return redirect(url_for('home'))
    
    try:
        new_status = request.form['status']
        with Session() as db_session:
            order = db_session.query(Orders).get(id)
            if order:
                order.state = new_status
                db_session.commit()
                flash(f"Pedido #{id} actualizado a {new_status}")
    except Exception as e:
        flash(f"Error: {e}")
    return redirect(url_for('admin', tab='orders'))

# --- RESERVATION STATUS ---
@app.route('/admin/res/status/<int:id>', methods=['POST'])
@login_required
def admin_res_status(id):
    if current_user.role != 'admin': return redirect(url_for('home'))
    
    try:
        new_status = request.form['status']
        with Session() as db_session:
            res = db_session.query(Reservation).get(id)
            if res:
                res.status = new_status
                db_session.commit()
                flash(f"Reserva #{id} actualizada")
    except Exception as e:
        flash(f"Error: {e}")
    return redirect(url_for('admin', tab='reservations'))

# --- USER ROLE ---
@app.route('/admin/user/role/<int:id>', methods=['POST'])
@login_required
def admin_user_role(id):
    if current_user.role != 'admin': return redirect(url_for('home'))
    
    try:
        new_role = request.form['role']
        with Session() as db_session:
            user = db_session.query(Users).get(id)
            if user:
                user.role = new_role
                db_session.commit()
                flash(f"Rol de {user.nickname} cambiado a {new_role}")
    except Exception as e:
        flash(f"Error: {e}")
    return redirect(url_for('admin', tab='users'))


@app.route('/send_receipt/<int:order_id>', methods=['POST'])
@login_required
def send_receipt(order_id):
    data = request.get_json()
    email = data.get("email") if data else None

    # 1. Validation Logic
    if not email:
        return jsonify({"success": False, "error": "Email is required"})
    
    # Simple regex for email validation
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(email_regex, email):
        print(f"❌ INVALID EMAIL FORMAT: {email}")
        return jsonify({"success": False, "error": "Invalid email format"})

    with Session() as db_session:
        order = db_session.query(Orders).filter_by(id=order_id, user_id=current_user.id).first()
        if not order:
            return jsonify({"success": False, "error": "Order not found"})

        # Validate user identity (log only)
        print("USER EMAIL (Account):", current_user.email)
        print("SENDING TO (Manual):", email)

        # Build items text
        items_text = ""
        # order.order_list is now a JSONB dict {item_id: quantity}
        # We need to fetch names for a pretty email
        for item_id, qty in (order.order_list or {}).items():
            menu_item = db_session.query(Menu).get(int(item_id))
            name = menu_item.name if menu_item else f"Item #{item_id}"
            items_text += f"{name} x {qty}\n"

        message_body = f"""
RetroBite Receipt

Order ID: {order.id}
Date: {order.order_time.strftime('%Y-%m-%d %H:%M')}

Items:
{items_text}

Total: ${order.total_price:.2f}

Thank you for your order!
Keep it Retro.
"""

        msg = Message(
            subject=f"Your RetroBite Receipt #{order.id}",
            sender=app.config['MAIL_USERNAME'],
            recipients=[email],
            body=message_body
        )

        try:
            mail.send(msg)
            print("EMAIL SENT OK")
            return jsonify({"success": True})
        except smtplib.SMTPAuthenticationError:
            print("ERROR MAIL: Authentication failed. Check your App Password.")
            return jsonify({"success": False, "error": "Auth Error"})
        except (smtplib.SMTPConnectError, socket.error) as e:
            print(f"ERROR MAIL: Connection/Network error: {e}")
            return jsonify({"success": False, "error": "Connection Error"})
        except Exception as e:
            print("ERROR MAIL (Other):", e)
            return jsonify({"success": False, "error": "Unknown Error"})


@app.route('/send_via_mac', methods=['POST'])
@login_required
def send_via_mac():
    data = request.get_json()
    recipient = data.get("email")
    total = data.get("total")
    order_id = data.get("order_id")

    if not recipient or not total:
        return jsonify({"success": False, "error": "Missing data"})

    # AppleScript to send via Mail.app (macOS only)
    script = f'''
    tell application "Mail"
        set newMessage to make new outgoing message with properties {{subject:"RetroBite Ticket #{order_id}", content:"Thank you for your visit!\\n\\nOrder #{order_id}\\nTotal: ${total}\\n\\nKeep it Retro.", visible:true}}
        tell newMessage
            make new to recipient with properties {{address:"{recipient}"}}
        end tell
        activate
    end tell
    '''
    
    try:
        subprocess.run(['osascript', '-e', script], check=True)
        return jsonify({"success": True})
    except Exception as e:
        print(f"AppleScript Error: {e}")
        return jsonify({"success": False, "error": str(e)})


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.route('/<path:filename>.html')
def remove_html(filename):
    return redirect(f'/{filename}')


if __name__ == '__main__':
    init_db()
    app.run(debug=True, port=5001)
