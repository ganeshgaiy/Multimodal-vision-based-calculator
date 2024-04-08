from flask import Flask, render_template, Response
import cv2

app = Flask(__name__)

global cam
cam = cv2.VideoCapture(0)

@app.route('/video')
def video():
    global cam
    cam = cv2.VideoCapture(0)
    return Response(frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

def frames():
    while True:
        success, img = cam.read()
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', img)
            img = buffer.tobytes()
            yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + img + b'\r\n') 

if __name__ == '__main__':
    app.run(debug=True)
