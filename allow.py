from speech import speak_from_queue, speech_queue
import threading


ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

Known_employee_encodings = []
Known_employee_names = []
Known_employee_rolls = []

# Jalankan thread untuk memutar suara dari antrian
speech_thread = threading.Thread(target=speak_from_queue, args=(speech_queue,))
speech_thread.daemon = True  # Mengatur thread sebagai daemon agar berhenti saat aplikasi berhenti
speech_thread.start()