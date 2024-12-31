# models/user.py
from . import db

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    nama = db.Column(db.String(100))
    username = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(200))  # Simpan password dalam bentuk plaintext
    role = db.Column(db.String(50))

    # Tidak ada fungsi hashing