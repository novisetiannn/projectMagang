# controllers/attendance.py
from flask import Blueprint, flash, render_template, request, send_file, redirect, url_for, session
import logging
from decorators.decorators import role_required
from database import get_db_connection  # Ganti dengan nama modul Anda
import face_recognition
import base64
import cv2
import os
import pandas as pd
import pickle
from fattendance import bisa_absen_lagi, recognize_faces
import queue 


attendancee = Blueprint('attendancee', __name__)

# Inisialisasi antrian suara
speech_queue = queue.Queue()
error_announced = False  # Variabel global untuk melacak apakah error telah diumumkan
error_timestamp = None  # Variabel waktu untuk membatasi pengulangan error

@attendancee.route('/attendance', methods=['GET', 'POST'])
def attendance():
    global error_announced, error_timestamp
    
    if request.method == 'POST':
        try:
            frame_data = request.form.get('frame')
            employee_id = request.form.get('employee_id')  # Ambil ID karyawan dari form
            
            if not frame_data:
                logging.error("No frame data received")
                return render_template('attendance.html', message="No frame data received.")

            if frame_data.startswith('data:image/jpeg;base64,'):
                frame_data = frame_data.split(',')[1]
                img_data = base64.b64decode(frame_data)
                photo_filename = f"./Train/{employee_id}_attendance.jpg"
                
                # Simpan gambar ke file
                with open(photo_filename, 'wb') as f:
                    f.write(img_data)

                rgb_frame = cv2.imread(photo_filename)
                faces, names, rolls = recognize_faces(rgb_frame)

                if len(faces) > 0:
                    roll = rolls[0]

                    # Cek apakah wajah dikenali
                    if names[0] == "Unknown":
                        logging.info("Wajah tidak dikenali. Absensi tidak disimpan.")
                        return render_template('attendance.html', message="Wajah tidak dikenali.")

                    # Validasi apakah karyawan diperbolehkan untuk absen
                    if not bisa_absen_lagi(roll):
                        logging.info("Anda sudah absen dalam 10 menit terakhir.")
                        return render_template('attendance.html', message="Anda sudah absen dalam 10 menit terakhir.")

                    # Simpan data absensi ke database
                    try:
                        db_conn = get_db_connection()
                        cursor = db_conn.cursor()
                        cursor.execute(
                            "INSERT INTO absensi (id_karyawan, check_in, photo, nama) VALUES (%s, NOW(), %s, %s)",
                            (roll, photo_filename, employee_id)  # Menggunakan employee_id sebagai nama
                        )
                        db_conn.commit()
                        cursor.close()
                        db_conn.close()
                        logging.info("Absensi berhasil disimpan.")

                    except Exception as e:
                        logging.error(f"Error saving attendance data: {e}")
                        flash('Error menyimpan data absen')
                else:
                    logging.error("No face detected")
                    return render_template('attendance.html', message="Tidak ada wajah yang terdeteksi.")
            else:
                logging.error("Invalid frame format")
                return render_template('attendance.html', message="Format frame tidak valid.")
        except Exception as e:
            logging.error(f"Error processing attendance: {e}")
            return render_template('attendance.html', message="Terjadi kesalahan saat memproses absensi.")
    
    # Untuk permintaan GET, kembalikan template absensi
    return render_template('attendance.html')