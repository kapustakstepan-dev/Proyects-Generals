from flask import Blueprint, request, jsonify, session, render_template, redirect, url_for
from flask_login import login_required, current_user
from ..services.order_service import OrderService
import os
from supabase import create_client

orders_bp = Blueprint('orders', __name__)

# Initialize client (BFF pattern)
supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_KEY")
supabase = create_client(supabase_url, supabase_key)
order_service = OrderService(supabase)

@orders_bp.route('/create_order', methods=['GET', 'POST'])
@login_required
def create_order():
    basket = session.get('basket', {})
    if request.method == 'POST':
        result = order_service.create_order(current_user.id, basket)
        if result['success']:
            session.pop('basket', None)
            return jsonify(result)
        return jsonify(result), 400
        
    # GET logic (calculate total for preview)
    total_price = sum(float(v) for v in basket.values()) # Simplified for template
    return render_template('create_order.html', basket=basket, total_price=total_price)

@orders_bp.route('/my_orders')
@login_required
def my_orders():
    orders = order_service.get_user_orders(current_user.id)
    return render_template('my_reservations.html', orders=orders)
