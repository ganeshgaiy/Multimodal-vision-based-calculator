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

text = ""
k = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
idset = ["", "1", "12", "123", "1234", "01234", "0", "01", "012", "0123", "04", "4", "34", "014", "14", "234"]
op = ["", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "+", "-", "*", "/"]

def frames():
    while True:
        if len(y) > 20:
            id = ""
            # Gesture recognition logic
            # Update text variable based on recognized gestures

            cv2.putText(img, text, (100, 120), cv2.FONT_HERSHEY_TRIPLEX, 3, (0, 0, 0), 5)
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

@app.route('/close')
def close():
    global cam
    cam.release()
    cv2.destroyAllWindows()
    return render_template("index.html")

@app.route('/')
def index():
    return render_template('index.html')

# Final cleanup and testing of the application. Ensure all routes work and video feed displays correctly.

if __name__ == '__main__':
    app.run(debug=True)
