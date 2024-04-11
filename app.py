from flask import Flask, render_template, Response
import cv2
import mediapipe as mp

app = Flask(__name__)

mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils

global cam
cam = cv2.VideoCapture(0)


x = []
y = []

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
                    for id, lm in enumerate(handLms.landmark):
                        h, w, c = img.shape
                        if id == 0:
                            x = []
                            y = []
                        x.append(int((lm.x) * w))
                        y.append(int((1 - lm.y) * h))


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
