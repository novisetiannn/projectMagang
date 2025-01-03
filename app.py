# app.py
from flask import Flask
from models import db
from controllers.auth import auth
from controllers.dashboard import dashboard
from controllers.tampil_data import tampil_data
from controllers.update_data import update_data
from controllers.hapus_data import hapus_data
from controllers.table import table
from controllers.upload import upload
from controllers.attendance import attendancee
from controllers.report import report
from controllers.video import vid
from loadknown import load_known_faces
from allow import Known_employee_encodings

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:2655@localhost:5432/attendance'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'supersecretkey'

db.init_app(app)
app.register_blueprint(auth)
app.register_blueprint(dashboard)
app.register_blueprint(tampil_data)
app.register_blueprint(update_data)
app.register_blueprint(hapus_data)
app.register_blueprint(table)
app.register_blueprint(upload, url_prefix='/upload')
app.register_blueprint(attendancee)
app.register_blueprint(vid)
app.register_blueprint(report)

if __name__ == "_main_":
    load_known_faces()
    app.run(host='127.0.0.1', port=5000, debug=True)