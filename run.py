from flask import Flask, escape, request, jsonify, make_response, render_template, render_template, Response
import requests
import json
import uuid
from flask_cors import CORS
import cv2
import os
import shutil
import time
import pyscreenshot as ImageGrab
import threading
import requests
from datetime import datetime,timezone,timedelta
tz = timezone(timedelta(hours=+8))


# 子執行緒的工作函數
def job():
  while True:
    key = GetMAC()
    memorydata = os.popen('free -h')
    image = ImageGrab.grab()
    image.save("fullscreen.png")
    time.sleep(10)
    image = cv2.imread('fullscreen.png')
    font = cv2.FONT_HERSHEY_SIMPLEX
    memstr = memorydata.read()
    memarr  = memstr.split('\n')
    memarr.append(datetime.today().astimezone(tz).strftime('%Y-%m-%d %HH:%MM:%SS'))
    y = 50
    
    for str in memarr:
        cv2.putText(image, text=str, org=(50, y), fontFace=font, fontScale=1, thickness=1, lineType=cv2.LINE_AA, color=(0, 0, 255))
        y+=50
    image = cv2.resize(image, (int(image.shape[1]*0.5), int(image.shape[0]*0.5)), interpolation=cv2.INTER_AREA)
    cv2.imwrite("out.jpg",image)
    url = "https://fit.raibaseserver.intemotech.com/device/devicePhoto"

    payload={'key': key}
    files=[
    ('file',('out.jpg',open('out.jpg','rb'),'image/jpeg'))
    ]
    headers = {}

    response = requests.request("POST", url, headers=headers, data=payload, files=files)

    print(response.text)

    
app = Flask(__name__)
app.config["DEBUG"] = True
app.config['SECRET_KEY'] = 'secret!'
CORS(app, supports_credentials=True)


def GetMAC():
    r""" 針對單網卡 """
    addr = hex(uuid.getnode())[2:].upper()
    return '-'.join(addr[i:i+2] for i in range(0, len(addr), 2))

@app.route('/')
def hello():
    return GetMAC()

# 串流測試


@app.route('/show')
def show():
    """Video streaming home page."""
    return render_template('show.html')


def gen():
    """Video streaming generator function."""
    path = "shm/"
    source_filefile = "tmp.jpg"
    file = "tmp1.jpg"
    
    while True:
        shutil.copyfile(os.path.join(path, source_filefile), os.path.join(path, file))
        with open(os.path.join(path, file), 'rb') as f:
            check_chars = f.read()[-2:]
        if check_chars != b'\xff\xd9':
            print('Not complete image')
        else:
            # imrgb = cv2.imread(os.path.join(path, file), 1)
            frame = cv2.imread(os.path.join(path, file))
            print(str(frame.shape))
            # frame = cv2.imread("1632733883.6317217tmp.jpg")
            try:
                ret, jpeg = cv2.imencode('.jpg', frame)
            except:
                continue
            yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n')


@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')
# 建立一個子執行緒
t = threading.Thread(target = job)

# 執行該子執行緒
t.start()

app.run(host="0.0.0.0", port=3000)