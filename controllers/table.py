# controllers/table.py
from flask import Blueprint, render_template, request, redirect, url_for, session
import logging
from decorators.decorators import role_required
from database import get_db_connection  # Ganti dengan nama modul Anda

table = Blueprint('table', __name__)

@table.route('/table_admin')
@role_required(['admin'])  # Hanya mengizinkan admin
def table_admin():
    return fetch_absensi_data('table_admin.html')

@table.route('/table_superadmin')
@role_required(['super_admin'])  # Hanya mengizinkan super_admin
def table_superadmin():
    return fetch_absensi_data('table_superadmin.html')

def fetch_absensi_data(template_name):
    absensi_data = []  # Inisialisasi data absensi
    try:
        db_conn = get_db_connection()
        cursor = db_conn.cursor()

        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')

        # Query untuk mengambil data absensi
        query = "SELECT nama, id_karyawan, check_in, photo FROM absensi WHERE 1=1"
        params = []

        # Tambahkan filter berdasarkan tanggal
        if start_date and end_date:
            query += " AND check_in BETWEEN %s AND %s"
            params.extend([start_date, end_date])

        cursor.execute(query, params)
        absensi_data = cursor.fetchall()

    except Exception as e:
        logging.error(f"Error fetching attendance data: {e}")
    finally:
        cursor.close()
        db_conn.close()

    # Menyediakan data ke template
    return render_template(template_name, data=absensi_data)
