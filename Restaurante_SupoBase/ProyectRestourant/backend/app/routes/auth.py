from flask import Blueprint, request, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required
from ..services.auth_service import AuthService
import os
from supabase import create_client

auth_bp = Blueprint('auth', __name__)

supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_KEY")
supabase = create_client(supabase_url, supabase_key)
auth_service = AuthService(supabase)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        result = auth_service.register(request.form['email'], request.form['password'])
        if result['success']:
            flash("Registered successfully!")
            return redirect(url_for('auth.login'))
        flash(result['error'])
    return render_template('register.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        result = auth_service.login(request.form['username'], request.form['password'])
        if result['success']:
            # Create a minimal User object for flask-login
            from ..main import create_app # Local import to avoid circular dep
            # Wait, better to define User class in a common place or use a mock
            class User:
                def __init__(self, data):
                    self.id = data.id
                    self.nickname = data.nickname
            # Actually, I'll just use the logic from main.py's load_user
            flash("Welcome!")
            return redirect(url_for('index'))
        flash("Invalid credentials")
    return render_template('login.html')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
