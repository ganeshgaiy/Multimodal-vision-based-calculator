from flask import Flask, render_template, Response
import cv2
import mediapipe as mp

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

app = Flask(__name__)

def frames():
    """
    Generator function that processes frames from a camera feed and yields them as JPEG images.

    Yields:
        bytes: JPEG image frame

    """
    while True:
        success, img = cam.read()
        if not success:
            break
        else:
            imgg = cv2.flip(img, 1)
            imgRGB = cv2.cvtColor(imgg, cv2.COLOR_BGR2RGB)
            results = hands.process(imgRGB)

            if results.multi_hand_landmarks:
                for handLms in results.multi_hand_landmarks:
                    for id, lm in enumerate(handLms.landmark):
                        h, w, c = imgg.shape
                        if id == 0:
                            x = []
                            y = []
                        x.append(int((lm.x) * w))
                        y.append(int((1 - lm.y) * h))

                        if len(y) > 20:
                            id = ""
                            big = [x[3], y[8], y[12], y[16], y[20]]
                            small = [x[4], y[6], y[10], y[14], y[18]]

                            for i in range(len(big)):
                                if big[i] > small[i]:
                                    id += str(i)

                            k[idset.index(id)] += 1

                            for i in range(len(k)):
                                if k[i] > 20:
                                    if i == 15:
                                        ans = str(eval(text))
                                        text = "= " + ans
                                        for i in range(len(k)):
                                            k[i] = 0
                                    else:
                                        text += op[i]
                                        for i in range(len(k)):
                                            k[i] = 0

                    cv2.putText(imgg, text, (100, 120), cv2.FONT_HERSHEY_TRIPLEX, 3, (0, 0, 0), 5)
                    mpDraw.draw_landmarks(imgg, handLms, mpHands.HAND_CONNECTIONS)

            else:
                text = " "

            ret, buffer = cv2.imencode('.jpg', imgg)
            imgg = buffer.tobytes()
            yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + imgg + b'\r\n')


@app.route('/video')
def video():
    global cam
    cam = cv2.VideoCapture(0)
    return Response(frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/close')
def close():
    global cam
    cam.release()
    cv2.destroyAllWindows()
    return render_template("index.html")


@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)