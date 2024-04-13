from flask import Flask, render_template, Response
import cv2
import mediapipe as mp
import time

app = Flask(__name__)

# Global variables setup
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1)
mp_draw = mp.solutions.drawing_utils
cam = cv2.VideoCapture(0)

id_set = ["", "1", "12", "123", "1234", "01234", "0", "01", "012", "0123", "04", "4", "34", "014", "14", "234"]
operations = ["", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "+", "-", "*", "/"]

# Initialize count array and text outside of the frames function to maintain state
k = [0] * len(id_set)
display_text = ""
eval_text = ""
last_update_time = time.time()
result_displayed = False

def frames():
    global k, display_text, eval_text, last_update_time, result_displayed

    while True:
        success, img = cam.read()
        if not success:
            break
        img = cv2.flip(img, 1)
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = hands.process(img_rgb)

        if results.multi_hand_landmarks:
            if result_displayed and (time.time() - last_update_time > 2):
                display_text = ""
                eval_text = ""
                result_displayed = False

            hand_lms = results.multi_hand_landmarks[0]
            h, w, c = img.shape
            x = [int(lm.x * w) for lm in hand_lms.landmark]
            y = [int((1 - lm.y) * h) for lm in hand_lms.landmark]

            if len(y) > 20:
                id = ""
                big = [x[3], y[8], y[12], y[16], y[20]]
                small = [x[4], y[6], y[10], y[14], y[18]]

                for i in range(len(big)):
                    if big[i] > small[i]:
                        id += str(i)

                if id in id_set:
                    k[id_set.index(id)] += 1

                    for i in range(len(k)):
                        if k[i] > 20:
                            if i == 15:  # Assuming 15 corresponds to 'evaluate'
                                try:
                                    ans = str(eval(eval_text))
                                    display_text = "= " + ans
                                    result_displayed = True
                                except Exception as e:
                                    display_text = "Error"
                                    result_displayed = True
                                eval_text = ""  # Reset eval_text after evaluation or error
                            else:
                                display_text += operations[i]
                                eval_text += operations[i]
                            k = [0] * len(k)
                            last_update_time = time.time()

            cv2.putText(img, display_text, (100, 120), cv2.FONT_HERSHEY_TRIPLEX, 3, (0, 0, 0), 5)
            mp_draw.draw_landmarks(img, hand_lms, mp_hands.HAND_CONNECTIONS)

        ret, buffer = cv2.imencode('.jpg', img)
        frame_bytes = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

@app.route('/video')
def video():
    return Response(frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/close')
def close():
    cam.release()
    cv2.destroyAllWindows()
    return "Camera and all resources were released, goodbye!"
    

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True, threaded=True)
