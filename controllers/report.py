# controllers/report.py
from flask import Blueprint, render_template, request, send_file, redirect, url_for, session
import logging
from decorators.decorators import role_required
from database import get_db_connection  # Ganti dengan nama modul Anda
import uuid
import time
import pdfkit
import os
import pandas as pd
from utils import image_to_base64

report = Blueprint('report', __name__)

@report.route('/report_admin')
@role_required(['admin'])  # Mengizinkan hanya admin
def report_admin():
    try:
        db_conn = get_db_connection()
        cursor = db_conn.cursor()
        
        cursor.execute("SELECT nama, id_karyawan, check_in FROM absensi")
        report_data = cursor.fetchall()
        
        cursor.close()
        db_conn.close()
        
        if not report_data:
            logging.warning("No data found for attendance report for admin.")
    except Exception as e:
        logging.error(f"Error fetching attendance report data for admin: {e}")
        report_data = []

    return render_template('report_admin.html', report_data=report_data)

@report.route('/report_superadmin')
@role_required(['super_admin'])  # Mengizinkan hanya super_admin
def report_super_admin():
    try:
        db_conn = get_db_connection()
        cursor = db_conn.cursor()
        
        cursor.execute("SELECT nama, id_karyawan, check_in FROM absensi")
        report_data = cursor.fetchall()
        
        cursor.close()
        db_conn.close()
        
        if not report_data:
            logging.warning("No data found for attendance report for super admin.")
    except Exception as e:
        logging.error(f"Error fetching attendance report data for super admin: {e}")
        report_data = []

    return render_template('report_superadmin.html', report_data=report_data)

@report.route('/report/download')
@role_required(['admin', 'super_admin'])  # Mengizinkan admin dan super_admin
def download_report():
    format_type = request.args.get('format')
    try:
        logging.info(f"Requested format: {format_type}")
        
        # Koneksi ke database
        db_conn = get_db_connection()
        cursor = db_conn.cursor()
        
        # Query untuk mengambil data absensi
        cursor.execute("SELECT nama, id_karyawan, check_in FROM absensi")
        report_data = cursor.fetchall()
        
        logging.info(f"Fetched report data: {report_data}")

        cursor.close()
        db_conn.close()

        if not report_data:
            return "No data available to generate report", 404

        # Generate laporan dalam format PDF
        if format_type == 'pdf':
            html_content = render_template('report_pdf.html', report_data=report_data)
            path_wkhtmltopdf = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'
            config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)
            
            # Nama file PDF yang unik
            pdf_file_path = f'laporan_absensi_{uuid.uuid4()}.pdf'
            pdf = pdfkit.from_string(html_content, False, configuration=config)
            
            with open(pdf_file_path, 'wb') as f:
                f.write(pdf)

            response = send_file(
                pdf_file_path,
                as_attachment=True,
                download_name='laporan_absensi.pdf'
            )

            # Tunggu sejenak sebelum menghapus file
            time.sleep(1)
            try:
                os.remove(pdf_file_path)
            except Exception as e:
                logging.error(f"Error removing PDF file: {e}")

            return response

        # Generate laporan dalam format Excel
        elif format_type == 'excel':
            # Konversi data ke DataFrame
            df = pd.DataFrame(report_data, columns=['Nama Karyawan', 'ID Karyawan', 'Waktu Check-in'])
            excel_file_path = f'laporan_absensi_{uuid.uuid4()}.xlsx'  # Nama file unik

            # Simpan data ke file Excel
            df.to_excel(excel_file_path, index=False)

            response = send_file(
                excel_file_path,
                as_attachment=True,
                download_name='laporan_absensi.xlsx'
            )

            # Tunggu sejenak sebelum menghapus file
            time.sleep(1)
            try:
                os.remove(excel_file_path)
            except Exception as e:
                logging.error(f"Error removing Excel file: {e}")

            return response

        # Format tidak valid
        else:
            return "Format tidak valid", 400
    except Exception as e:
        logging.error(f"Error generating report: {e}")
        return "Error generating report", 500