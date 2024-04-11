from flask import Flask, render_template, Response
import cv2
import mediapipe as mp

app = Flask(__name__)

mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils

global cam
cam = cv2.VideoCapture(0)


def frames():
    while True:
        success, img = cam.read()
        if not success:
            break
        else:
            imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            results = hands.process(imgRGB)

            if results.multi_hand_landmarks:
                for handLms in results.multi_hand_landmarks:
                    mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)

            ret, buffer = cv2.imencode('.jpg', img)
            img = buffer.tobytes()
            yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + img + b'\r\n') 

            
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
