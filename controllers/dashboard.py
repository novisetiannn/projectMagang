# controllers/dashboard.py
from flask import Blueprint, render_template, session, redirect, url_for
from models.user import User
from models.employee import Employee

dashboard = Blueprint('dashboard', __name__)

@dashboard.route('/')
def home():
    return render_template('home.html')

@dashboard.route('/admin_dashboard')
def admin_dashboard():
    if 'username' not in session or session.get('role') != 'admin':
        return redirect(url_for('auth.login'))
    
    total_pengguna = User.query.count()
    total_karyawan = Employee.query.count()
    users = Employee.query.all()
    return render_template('admin_dashboard.html', 
                           username=session['username'], 
                           total_pengguna=total_pengguna, 
                           total_karyawan=total_karyawan, 
                           users=users)

@dashboard.route('/super_admin_dashboard')
def super_admin_dashboard():
    if 'username' not in session or session.get('role') != 'super_admin':
        return redirect(url_for('auth.login'))

    total_pengguna = User.query.count()
    total_admin = User.query.filter_by(role='admin').count()
    users = User.query.order_by(User.id.desc()).limit(10).all()
    return render_template('super_admin_dashboard.html', 
                           total_pengguna=total_pengguna, 
                           total_admin=total_admin, 
                           users=users,
                           nama=session['username'])

@dashboard.route('/user_dashboard')
def user_dashboard():
    if 'username' not in session:
        return redirect(url_for('auth.login'))
    return render_template('user_dashboard.html')