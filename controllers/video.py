# controllers/video.py
from flask import Blueprint, Response, flash, render_template, request, send_file, redirect, url_for, session
import logging
from generate_marked_frames import generate_marked_frames

vid = Blueprint('vid', __name__)

@vid.route('/video')
def video():
    return Response(generate_marked_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')