from flask import Blueprint, Response
from .controller import generate_frames

analysis = Blueprint('analysis', __name__)


@analysis.route('/')
def index():
    return "Hello analysis"


@analysis.route('/video_feed', methods=['GET'])
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')