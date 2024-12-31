# controllers/update_data.py
from flask import Blueprint, render_template, request, redirect, url_for, session
import logging
from decorators.decorators import role_required
from database import get_db_connection  # Ganti dengan nama modul Anda

update_data = Blueprint('update_data', __name__)

@update_data.route('/update_employee_superadmin/<int:id_karyawan>', methods=['GET', 'POST'])
@role_required(['super_admin'])
def update_employee_superadmin(id_karyawan):
    db_conn = get_db_connection()
    cursor = db_conn.cursor()

    if request.method == 'POST':
        nama = request.form['nama']
        
        try:
            update_by = session.get('user_name')

            cursor.execute("""
                UPDATE employee 
                SET name = %s, tgl_update = CURRENT_TIMESTAMP, update_by = %s
                WHERE id_karyawan = %s
            """, (nama, update_by, id_karyawan))
            db_conn.commit()
            return redirect(url_for('tampil_data.tampil_data_superadmin'))
        except Exception as e:
            logging.error(f"Error updating employee data: {e}")
            db_conn.rollback()
            return "An error occurred while updating the employee data.", 500
        finally:
            cursor.close()
            db_conn.close()

    cursor.execute("SELECT * FROM employee WHERE id_karyawan = %s", (id_karyawan,))
    karyawan = cursor.fetchone()

    cursor.close()
    db_conn.close()

    return render_template('update_employee_superadmin.html', karyawan=karyawan)


@update_data.route('/update_employee_admin/<int:id_karyawan>', methods=['GET', 'POST'])
@role_required(['admin'])
def update_employee_admin(id_karyawan):
    db_conn = get_db_connection()
    cursor = db_conn.cursor()

    if request.method == 'POST':
        new_name = request.form['name']
        try:
            update_by = session.get('user_name')

            cursor.execute("""
                UPDATE employee 
                SET name = %s, update_by = %s
                WHERE id_karyawan = %s
            """, (new_name, update_by, id_karyawan))
            db_conn.commit()
            return redirect(url_for('tampil_data.tampil_data_admin'))
        except Exception as e:
            logging.error(f"Error updating employee name: {e}")
            db_conn.rollback()
            return "An error occurred while updating the employee name.", 500
        finally:
            cursor.close()
            db_conn.close()

    cursor.execute("""
        SELECT id_karyawan, name
        FROM employee 
        WHERE id_karyawan = %s
    """, (id_karyawan,))
    employee_data = cursor.fetchone()

    cursor.close()
    db_conn.close()

    if employee_data is None:
        return redirect(url_for('tampil_data.tampil_data_admin'))

    return render_template('update_employee_admin.html', employee_data=employee_data)