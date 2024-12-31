import cv2
import logging
from fattendance import recognize_faces, bisa_absen_lagi
from database import get_db_connection
from speech import speech_queue
from datetime import datetime, timedelta


#fungsi untuk Mengambil video dari kamera, mengenali wajah, dan menandai hasilnya di frame.
def generate_marked_frames():
    # sourcery skip: low-code-quality, merge-else-if-into-elif, swap-if-else-branches
    global error_announced, error_timestamp
    camera = cv2.VideoCapture(0)  # Pastikan indeks kamera benar
    recognized_names = set()  # Set untuk menyimpan nama yang sudah dikenali
    unknown_face_alerted = False  # Penanda untuk suara wajah tidak dikenali
    frame_skip = 5  # Proses setiap frame ke-5
    frame_count = 0

    while True:
        success, frame = camera.read()
        if not success:
            logging.error("Gagal menangkap frame dari kamera.")
            break
        
        frame_count += 1
        
        # Lewati pemrosesan untuk frame tertentu
        if frame_count % frame_skip != 0:
            continue

        # Ubah ukuran frame untuk mengurangi waktu pemrosesan
        frame = cv2.resize(frame, (320, 240))  # Sesuaikan ukuran sesuai kebutuhan

        faces, names, rolls = recognize_faces(frame)

        found_unknown = False  # Penanda untuk wajah yang tidak dikenali

        for (top, right, bottom, left), name, roll in zip(faces, names, rolls):
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
            cv2.putText(frame, f"{name} ({roll})", (left, bottom + 30), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (36, 255, 12), 2)

            if name != "Unknown":
                # Reset penanda untuk wajah tidak dikenali jika wajah dikenali
                unknown_face_alerted = False
                
                # Periksa apakah pengguna bisa absen lagi dalam waktu 10 menit
                if not bisa_absen_lagi(roll):
                    if name not in recognized_names:
                        speech_queue.put("Akses diterima, terima kasih")  # Suara jika sudah absen dalam 10 menit terakhir
                        recognized_names.add(name)
                else:
                    # Simpan foto dan data ke database jika absen diperbolehkan
                    photo_filename = f"./Train/{name}_attendance.jpg"
                    cv2.imwrite(photo_filename, frame)

                    try:
                        db_conn = get_db_connection()
                        cursor = db_conn.cursor()
                        cursor.execute(
                            "INSERT INTO absensi (nama, id_karyawan, check_in, photo) VALUES (%s, %s, NOW(), %s)",
                            (name, roll, photo_filename)
                        )
                        db_conn.commit()
                        cursor.close()
                        db_conn.close()
                        speech_queue.put("Berhasil")
                        recognized_names.add(name)
                    except Exception as e:
                        logging.error(f"Error menyimpan data absen: {e}")
                        current_time = datetime.now()

                        # Pastikan error hanya diumumkan sekali dalam interval 10 menit
                        if not error_announced or (error_timestamp and (current_time - error_timestamp).total_seconds() > 600):
                            speech_queue.put("Error menyimpan data absen")
                            error_announced = True
                            error_timestamp = current_time
            else:
                # Jika wajah tidak dikenali, set flag dan putar suara
                found_unknown = True

        # Cek jika ada wajah yang tidak dikenali
        if found_unknown:
            if not unknown_face_alerted:  # Pastikan suara hanya diputar sekali
                speech_queue.put("Silahkan coba lagi")  # Suara jika wajah tidak dikenali
                unknown_face_alerted = True  # Set flag menjadi True
        else:
            # Reset penanda untuk wajah tidak dikenali jika ada wajah yang dikenali
            unknown_face_alerted = False

        # Mengubah frame ke format yang bisa dikirim
        ret, buffer = cv2.imencode('.jpg', frame)
        if not ret:
            logging.error("Gagal mengubah frame ke format JPEG.")
            break
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    camera.release()