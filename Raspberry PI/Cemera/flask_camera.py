import io
import picamera
from flask import Flask, Response

app = Flask(__name__)

def generate_frame():
    with picamera.PiCamera() as camera:
        camera.resolution = (640,480)
        camera.framerate = 16
        stream = io.BytesIO()

        for _ in camera.capture_continuous(stream, 'jpeg', use_video_port=True):
            stream.seek(0)
            yield b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + stream.read()+ b'\r\n'
            stream.seek(0)
            stream.truncate()

@app.route('/video_feed')
def video_feed():
    return Response(generate_frame(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port = 12344, threaded=True)

    #wchodzimy  wprzeglądarkę i wpisujemy:
    #adress_RPI:12344/video_feed
