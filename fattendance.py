import logging
from database import get_db_connection
from datetime import datetime, timedelta
import cv2
import face_recognition
from allow import allowed_file, Known_employee_encodings, Known_employee_rolls, Known_employee_names
import numpy as np

# fungsi untuk Memeriksa apakah karyawan dapat melakukan absensi lagi dalam waktu 10 menit setelah absensi terakhir.
def bisa_absen_lagi(roll):
    try:
        db_conn = get_db_connection()
        cursor = db_conn.cursor()
        
        # Ambil waktu absensi terakhir dari database
        cursor.execute(
            "SELECT check_in FROM absensi WHERE id_karyawan = %s ORDER BY check_in DESC LIMIT 1",
            (roll,)
        )
        last_attendance = cursor.fetchone()
        cursor.close()
        db_conn.close()

        if last_attendance:
            last_attendance_time = last_attendance[0]  # Waktu absensi terakhir
            current_time = datetime.now()  # Waktu saat ini

            # Selisih waktu
            time_difference = current_time - last_attendance_time

            # Cek jika selisih waktu kurang dari 10 menit
            if time_difference < timedelta(minutes=10):
                logging.info("Belum 10 menit sejak absen terakhir. Tidak bisa absen.")
                return False  # Belum 10 menit, tidak boleh absen
        return True  # Bisa absen jika tidak ada riwayat atau lebih dari 10 menit
    except Exception as e:
        logging.error(f"Terjadi kesalahan saat mengambil data absen terakhir: {e}")
        return False
    
# Fungsi untuk mendeteksi dan mengenali wajah
def recognize_faces(frame):
    # Ubah frame ke RGB
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    # Deteksi lokasi wajah
    face_locations = face_recognition.face_locations(rgb_frame)
    
    # Ekstrak encoding wajah
    face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

    names = []
    rolls = []

    # Log jika tidak ada wajah terdeteksi
    if len(face_encodings) == 0:
        logging.warning("No faces detected in the frame.")
        return face_locations, names, rolls

    # Iterasi setiap encoding wajah
    for face_encoding in face_encodings:
        # Log encoding wajah yang baru
        logging.info(f"New face encoding: {face_encoding}")

        # Hitung jarak antara wajah baru dan encoding yang dikenal
        face_distances = face_recognition.face_distance(Known_employee_encodings, face_encoding)
        
        # Log jarak wajah
        logging.debug(f"Face distances: {face_distances}")
        
        # Tangani jika `Known_employee_encodings` kosong
        if len(face_distances) == 0:
            logging.warning("No known encodings available for comparison.")
            name = "Unknown"
            roll = "Unknown"
        else:
            # Cari indeks kecocokan terbaik
            best_match_index = np.argmin(face_distances)
            
            # Validasi jarak terbaik terhadap threshold
            if face_distances[best_match_index] < 0.4:  # Sesuaikan threshold jika perlu
                name = Known_employee_names[best_match_index]
                roll = Known_employee_rolls[best_match_index]
            else:
                name = "Unknown"
                roll = "Unknown"

        # Tambahkan hasil ke list
        names.append(name)
        rolls.append(roll)

        # Log hasil pencocokan
        logging.info(f"Matched name: {name}, roll: {roll}")

    return face_locations, names, rolls
