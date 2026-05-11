from flask import Blueprint, render_template
from ..services.menu_service import MenuService
import os
from supabase import create_client

menu_bp = Blueprint('menu', __name__)

supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_KEY")
supabase = create_client(supabase_url, supabase_key)
menu_service = MenuService(supabase)

@menu_bp.route('/menu')
def view_menu():
    items = menu_service.get_active_menu()
    return render_template('menu.html', menu_items=items)
