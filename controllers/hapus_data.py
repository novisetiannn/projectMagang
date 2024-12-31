# controllers/update_data.py
from flask import Blueprint, render_template, request, redirect, url_for, session
import logging
from decorators.decorators import role_required
from database import get_db_connection  # Ganti dengan nama modul Anda

hapus_data = Blueprint('hapus_data', __name__)

@hapus_data.route('/hapus_karyawan/<int:id_karyawan>', methods=['POST'])
@role_required(['super_admin'])
def hapus_karyawan(id_karyawan):
    db_conn = get_db_connection()
    cursor = db_conn.cursor()

    try:
        delete_by = session.get('user_name')

        cursor.execute("""
            UPDATE employee 
            SET tgl_delete = CURRENT_TIMESTAMP, delete_by = %s 
            WHERE id_karyawan = %s
        """, (delete_by, id_karyawan))
        db_conn.commit()

        # Cek apakah ada baris yang terpengaruh
        if cursor.rowcount == 0:
            logging.warning(f"No employee found with id_karyawan: {id_karyawan}")

    except Exception as e:
        logging.error(f"Error deleting employee: {e}")
        db_conn.rollback()
    finally:
        cursor.close()
        db_conn.close()

    return redirect(url_for('tampil_data.tampil_data_superadmin'))

@hapus_data.route('/hapus_karyawan_admin/<int:id_karyawan>', methods=['POST'])
@role_required(['admin'])
def hapus_karyawan_admin(id_karyawan):
    try:
        db_conn = get_db_connection()
        cursor = db_conn.cursor()

        delete_by = session.get('user_name')

        cursor.execute("""
            UPDATE employee 
            SET delete_by = %s
            WHERE id_karyawan = %s
        """, (delete_by, id_karyawan))
        db_conn.commit()

    except Exception as e:
        db_conn.rollback()
        logging.error(f"Error deleting employee: {e}")
        return "Terjadi kesalahan saat menghapus karyawan.", 500

    finally:
        cursor.close()
        db_conn.close()

    return redirect(url_for('tampil_data.tampil_data_admin'))