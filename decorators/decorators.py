# decorators/decorators.py
from functools import wraps
from flask import session, flash, redirect, url_for

def role_required(roles):
    # Pastikan roles adalah list jika hanya satu role yang diberikan
    if isinstance(roles, str):
        roles = [roles]

    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # Memeriksa apakah role pengguna ada di dalam roles yang diizinkan
            if session.get('role') not in roles:
                flash('You do not have permission to access this page.', 'error')
                return redirect(url_for('auth.login'))  # Ganti 'auth.login' dengan rute Anda
            return f(*args, **kwargs)
        return decorated_function
    return decorator