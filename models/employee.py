# models/employee.py
from . import db
import pickle

class Employee(db.Model):
    __tablename__ = 'employee'
    id_karyawan = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    face_encoding = db.Column(db.LargeBinary)
    photo = db.Column(db.Text)

    def set_face_encoding(self, encoding):
        self.face_encoding = pickle.dumps(encoding)

    def get_face_encoding(self):
        return pickle.loads(self.face_encoding)