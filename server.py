from flask import Flask, render_template, Response, jsonify, request
from camera import VideoCamera
import atexit
import os
from datetime import date


app = Flask(__name__)

if not os.path.exists('./static/videos'):
    os.makedirs('./static/videos')


first_frame=None
video_camera = None
global_frame = None


@atexit.register
def shutdown():
    if video_camera:
        video_camera.__del__()

def get_videos_for_today():
    directory = './static/videos/'

    today_str = date.today().strftime('%Y%m%d')  # '20231003' for October 3, 2023
    return [f for f in os.listdir(directory) if f.startswith('video_' + today_str)]


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/user')
def user():
    return render_template('user.html')
    
@app.route('/activity')
def activity():
    video_files = get_videos_for_today()
    return render_template('activity.html', video_files=video_files)

@app.route('/device')
def device():
    return render_template('device.html')

@app.route('/setting')
def setting():
    return render_template('setting.html')

@app.route('/record_status', methods=['POST'])
def record_status():
    global video_camera 
    if video_camera == None:
        video_camera = VideoCamera()

    json = request.get_json()

    status = json['status']

    if status == "true":
        video_camera.start_record()
        return jsonify(result="started")
    else:
        video_camera.stop_record()
        return jsonify(result="stopped")

def video_stream():
    global video_camera 
    global global_frame

    if video_camera == None:
        video_camera = VideoCamera()
        
    while True:
        frame = video_camera.get_frame()

        if frame != None:
            global_frame = frame
            yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
        else:
            yield (b'--frame\r\n'
                            b'Content-Type: image/jpeg\r\n\r\n' + global_frame + b'\r\n\r\n')

@app.route('/video_viewer')
def video_viewer():
    return Response(video_stream(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0',port='5003', threaded=True, debug = True)





