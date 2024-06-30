# Define application routes and view functions
from flask import Blueprint, render_template, request, jsonify, flash, redirect, url_for
from flask_login import login_user, current_user, logout_user, login_required
from app import db, bcrypt
from app.models import User
from app.services.deal_finder import find_deals

main = Blueprint('main', __name__)


@main.route('/')
def index():
    return render_template('index.html')


@main.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user:
            flash('Username already exists', 'danger')
        else:
            hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
            user = User(username=username, password=hashed_password)
            db.session.add(user)
            db.session.commit()
            flash('Account created successfully', 'success')
            return redirect(url_for('main.login'))
    return render_template('register.html')


@main.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('main.index'))
        else:
            flash('Login unsuccessful. Please check username and password', 'danger')
    return render_template('login.html')


@main.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))


@main.route('/search', methods=['POST'])
@login_required
def search():
    data = request.get_json()
    budget = data.get('budget')
    items = data.get('items')

    if not budget or not items:
        return jsonify({"message": "Budget and items are required"})

    results, total_cost = find_deals(float(budget), items)

    return jsonify({
        "results": results,
        "total_cost": total_cost,
        "remaining_budget": float(budget) - total_cost
    })

