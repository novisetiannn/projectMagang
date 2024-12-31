# controllers/upload.py
from flask import Blueprint, flash, render_template, request, send_file, redirect, url_for, session
import logging
from decorators.decorators import role_required
from database import get_db_connection  # Ganti dengan nama modul Anda
import face_recognition
import base64
import cv2
import os
import pandas as pd
from utils import image_to_base64
from allow import allowed_file, Known_employee_encodings, Known_employee_rolls, Known_employee_names
import pickle

upload = Blueprint('upload', __name__)

@upload.route('/upload_superadmin', methods=['GET', 'POST'])
@role_required(['super_admin'])
def upload_superadmin():  # sourcery skip: low-code-quality
    if request.method == 'POST':
        files = request.files.getlist('images')
        name = request.form['name']
        roll = request.form['roll']
        image_data = request.form.get('image_data')  # Ambil data gambar dari kamera jika ada

        saved_files = []

        # Validasi: Pastikan ada file dan tidak lebih dari 5
        if files and 1 <= len(files) <= 5 and name and roll:
            for idx, file in enumerate(files):
                if file and allowed_file(file.filename):
                    ext = file.filename.split('.')[-1]
                    stfilename = f"{name}_{roll}_{idx + 1}.{ext}"
                    
                    try:
                        file_path = os.path.join('./Train/', stfilename)
                        file.save(file_path)
                        saved_files.append(file_path)

                        newImg = cv2.imread(file_path)
                        if newImg is None:
                            os.remove(file_path)
                            return render_template('upload_superadmin.html', badImage=True)

                        face_encodings = face_recognition.face_encodings(cv2.cvtColor(newImg, cv2.COLOR_BGR2RGB))
                        if len(face_encodings) == 0:
                            os.remove(file_path)
                            return render_template('upload_superadmin.html', badImage=True)

                        newEncode = face_encodings[0]
                        Known_employee_encodings.append(newEncode)
                        Known_employee_names.append(name)
                        Known_employee_rolls.append(roll)

                    except Exception as e:
                        logging.error(f"Error processing file {file.filename}: {e}")
                        for file_path in saved_files:
                            if os.path.exists(file_path):
                                os.remove(file_path)
                        return render_template('upload_superadmin.html', badImage=True)

        # Proses gambar yang ditangkap dari kamera jika ada
        if image_data:
            img_data = image_data.split(',')[1]  # Mengambil data base64
            try:
                img_bytes = base64.b64decode(img_data)
                image_path = os.path.join('./Train/', f"{name}_{roll}_captured.jpg")
                with open(image_path, 'wb') as f:
                    f.write(img_bytes)

                saved_files.append(image_path)
                newImg = cv2.imread(image_path)
                if newImg is None:
                    os.remove(image_path)
                    return render_template('upload_superadmin.html', badImage=True)

                face_encodings = face_recognition.face_encodings(cv2.cvtColor(newImg, cv2.COLOR_BGR2RGB))
                if len(face_encodings) == 0:
                    os.remove(image_path)
                    return render_template('upload_superadmin.html', badImage=True)

                newEncode = face_encodings[0]
                Known_employee_encodings.append(newEncode)
                Known_employee_names.append(name)
                Known_employee_rolls.append(roll)

            except Exception as e:
                logging.error(f"Error processing captured image: {e}")
                if os.path.exists(image_path):
                    os.remove(image_path)
                return render_template('upload_superadmin.html', badImage=True)

        # Simpan ke database
        try:
            db_conn = get_db_connection()
            cursor = db_conn.cursor()

            saved_files_pg = "{" + ",".join([f'"{file_path}"' for file_path in saved_files]) + "}"
            face_encoding_bytes = pickle.dumps(newEncode)

            cursor.execute(
                "INSERT INTO employee (name, id_karyawan, face_encoding, photo) VALUES (%s, %s, %s, %s)",
                (name, roll, face_encoding_bytes, saved_files_pg)
            )

            db_conn.commit()
            cursor.close()
            db_conn.close()

            flash("Upload berhasil!", "success")  # Notifikasi sukses
            return redirect(url_for('upload_superadmin'))  # Redirect kembali ke halaman upload

        except Exception as e:
            logging.error(f"Error saving to database: {e}")
            for file_path in saved_files:
                if os.path.exists(file_path):
                    os.remove(file_path)
            return render_template('upload_superadmin.html', badImage=True)

    # Untuk permintaan GET, tidak lagi mengambil daftar region
    return render_template('upload_superadmin.html')

@upload.route('/upload_admin', methods=['GET', 'POST'])
@role_required(['admin'])  # Hanya mengizinkan admin
def upload_admin():  # sourcery skip: low-code-quality
    if request.method == 'POST':
        files = request.files.getlist('images')
        name = request.form['name']
        roll = request.form['roll']
        image_data = request.form.get('image_data')  # Ambil data gambar dari kamera jika ada

        saved_files = []

        # Validasi: Pastikan ada file dan tidak lebih dari 5
        if files and 1 <= len(files) <= 5 and name and roll:
            for idx, file in enumerate(files):
                if file and allowed_file(file.filename):
                    ext = file.filename.split('.')[-1]
                    stfilename = f"{name}_{roll}_{idx + 1}.{ext}"
                    
                    try:
                        file_path = os.path.join('./Train/', stfilename)
                        file.save(file_path)
                        saved_files.append(file_path)

                        newImg = cv2.imread(file_path)
                        if newImg is None:
                            os.remove(file_path)
                            return render_template('upload_admin.html', badImage=True)

                        face_encodings = face_recognition.face_encodings(cv2.cvtColor(newImg, cv2.COLOR_BGR2RGB))
                        if len(face_encodings) == 0:
                            os.remove(file_path)
                            return render_template('upload_admin.html', badImage=True)

                        newEncode = face_encodings[0]
                        Known_employee_encodings.append(newEncode)
                        Known_employee_names.append(name)
                        Known_employee_rolls.append(roll)

                    except Exception as e:
                        logging.error(f"Error processing file {file.filename}: {e}")
                        for file_path in saved_files:
                            if os.path.exists(file_path):
                                os.remove(file_path)
                        return render_template('upload_admin.html', badImage=True)

        # Proses gambar yang ditangkap dari kamera jika ada
        if image_data:
            img_data = image_data.split(',')[1]  # Mengambil data base64
            try:
                img_bytes = base64.b64decode(img_data)
                image_path = os.path.join('./Train/', f"{name}_{roll}_captured.jpg")
                with open(image_path, 'wb') as f:
                    f.write(img_bytes)

                saved_files.append(image_path)
                newImg = cv2.imread(image_path)
                if newImg is None:
                    os.remove(image_path)
                    return render_template('upload_admin.html', badImage=True)

                face_encodings = face_recognition.face_encodings(cv2.cvtColor(newImg, cv2.COLOR_BGR2RGB))
                if len(face_encodings) == 0:
                    os.remove(image_path)
                    return render_template('upload_admin.html', badImage=True)

                newEncode = face_encodings[0]
                Known_employee_encodings.append(newEncode)
                Known_employee_names.append(name)
                Known_employee_rolls.append(roll)

            except Exception as e:
                logging.error(f"Error processing captured image: {e}")
                if os.path.exists(image_path):
                    os.remove(image_path)
                return render_template('upload_admin.html', badImage=True)

        # Simpan ke database
        try:
            db_conn = get_db_connection()
            cursor = db_conn.cursor()

            saved_files_pg = "{" + ",".join([f'"{file_path}"' for file_path in saved_files]) + "}"
            face_encoding_bytes = pickle.dumps(newEncode)

            cursor.execute(
                "INSERT INTO employee (name, id_karyawan, face_encoding, photo) VALUES (%s, %s, %s, %s)",
                (name, roll, face_encoding_bytes, saved_files_pg)
            )

            db_conn.commit()
            cursor.close()
            db_conn.close()

            flash("Upload berhasil!", "success")  # Notifikasi sukses
            return redirect(url_for('upload_admin'))  # Redirect kembali ke halaman upload

        except Exception as e:
            logging.error(f"Error saving to database: {e}")
            for file_path in saved_files:
                if os.path.exists(file_path):
                    os.remove(file_path)
            return render_template('upload_admin.html', badImage=True)

    # Untuk permintaan GET, tidak lagi mengambil daftar region
    return render_template('upload_admin.html')