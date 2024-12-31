# controllers/auth.py
from flask import Blueprint, render_template, request, redirect, session, url_for
import logging
from passlib.hash import sha256_crypt
from database import get_db_connection
from models.user import User

auth = Blueprint('auth', __name__)

# @auth.route('/')
# def index():
#     if 'logged_in' in session:
#         try:
#             db_conn = get_db_connection()
#             cursor = db_conn.cursor()
            
#             cursor.execute("SELECT COUNT(*) FROM users")  # Pastikan tabel yang benar
#             total_pengguna = cursor.fetchone()[0]  # Ambil total pengguna
            
#             cursor.execute("SELECT * FROM users")  # Ambil semua pengguna
#             users = cursor.fetchall()
            
#             cursor.close()
#             db_conn.close()
#         except Exception as e:
#             logging.error(f"Error fetching user data: {e}")
#             total_pengguna = 0
#             users = []

#         return render_template('index.html', 
#                                nama=session.get('nama'), 
#                                username=session['username'], 
#                                total_pengguna=total_pengguna, 
#                                users=users)
#     else:
#         return redirect('/loginsignup')

@auth.route('/loginsignup')
def loginsignup():
    return render_template('login.html')

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Cek apakah ini adalah signup
        if 'usrup' in request.form:
            # Ini adalah signup
            username_up = request.form['usrup']
            password_up = request.form['pwdup']
            nama = request.form['nama']
            hashed_password = sha256_crypt.hash(password_up)

            try:
                db_conn = get_db_connection()
                cursor = db_conn.cursor()
                cursor.execute("INSERT INTO users (nama, username, password, role) VALUES (%s, %s, %s, %s)", 
                               (nama, username_up, hashed_password, 'user'))  # Atur role default
                db_conn.commit()
                cursor.close()
                db_conn.close()

                logging.info("New user signed up successfully.")
                # Langsung login setelah signup berhasil
                return redirect('/loginsignup')  # Redirect ke login setelah signup
            except Exception as e:
                logging.error(f"Database connection error during signup: {e}")
                return render_template('login.html', error_message='Database connection error')
        else:
            # Ini adalah login
            username = request.form['usr']  # Ambil username dari form
            password = request.form['pwd']    # Ambil password dari form

            try:
                db_conn = get_db_connection()
                cursor = db_conn.cursor()
                cursor.execute("SELECT password, role FROM users WHERE username = %s", (username,))
                result = cursor.fetchone()

                if result and sha256_crypt.verify(password, result[0]):
                    # Login berhasil
                    role = result[1]
                    session['username'] = username  # Simpan username di session
                    session['role'] = role  # Simpan role di session
                    session['logged_in'] = True  # Tandai user sebagai logged in
                    cursor.close()
                    db_conn.close()

                    # Redirect berdasarkan role
                    if role == 'admin':
                        return redirect('/admin_dashboard')
                    elif role == 'super_admin':
                        return redirect('/super_admin_dashboard')
                    else:
                        return redirect('/user_dashboard')  # Redirect untuk pengguna biasa
                else:
                    # Login gagal
                    cursor.close()
                    db_conn.close()
                    return render_template('login.html', error_message='Invalid username or password')
            except Exception as e:
                logging.error(f"Database connection error during login: {e}")
                return render_template('login.html', error_message='Database connection error')
    return render_template('login.html')