# controllers/tampil_data.py
from flask import Blueprint, render_template, session,request, redirect, url_for
from models.user import User
import logging
from database import get_db_connection
from models.employee import Employee
from decorators.decorators import role_required

tampil_data = Blueprint('tampil_data', __name__)

@tampil_data.route('/tampil_data_admin', methods=['GET'])
@role_required(['admin'])  # Hanya mengizinkan admin
def tampil_data_admin():
    search_query = request.args.get('search', '')  # Ambil kata kunci pencarian dari URL
    data_list = []
    
    try:
        db_conn = get_db_connection()
        cursor = db_conn.cursor()

        # Query SQL untuk mencari karyawan berdasarkan nama
        if search_query:
            cursor.execute("""
                SELECT id_karyawan, name
                FROM employee 
                WHERE LOWER(name) LIKE LOWER(%s)
            """, ('%' + search_query + '%',))  # Menambahkan wildcard '%' di sekitar kata kunci
        else:
            cursor.execute("""
                SELECT id_karyawan, name
                FROM employee
            """)

        data_list = cursor.fetchall()  # Ambil hasil query

    except Exception as e:
        logging.error(f"Error fetching employee data for admin: {e}")
        return "Terjadi kesalahan dalam mengambil data.", 500

    finally:
        cursor.close()
        db_conn.close()

    return render_template('tampil_data_admin.html', data_list=data_list)

@tampil_data.route('/tampil_data_superadmin', methods=['GET'])
@role_required(['super_admin'])  # Hanya mengizinkan super_admin
def tampil_data_superadmin():
    data_list = []
    query = request.args.get('query', '')  # Ambil parameter pencarian
    
    try:
        db_conn = get_db_connection()
        cursor = db_conn.cursor()
        
        # Query dengan filter pencarian yang tidak case sensitive
        if query:
            cursor.execute("""
                SELECT * 
                FROM employee 
                WHERE LOWER(name) LIKE LOWER(%s) 
                ORDER BY tgl_create DESC
            """, (f"%{query}%",))
        else:
            cursor.execute("SELECT * FROM employee ORDER BY tgl_create DESC")
        
        data_list = cursor.fetchall()
    except Exception as e:
        logging.error(f"Error fetching employee data for superadmin: {e}")
    finally:
        cursor.close()
        db_conn.close()

    return render_template('tampil_data_superadmin.html', data_list=data_list)