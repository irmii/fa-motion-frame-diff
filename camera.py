import cv2
import time
from datetime import datetime

import smtplib

def send_email(message):
    sender = "mail_from@gmail.com"
    password = "pass"
    recipient = "mail_to@gmail.com"

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()

    server.login(sender, password)
    server.sendmail(sender, recipient, message)




class VideoCamera(object):
    def __init__(self):
        self.cap = cv2.VideoCapture(0)
        self.is_record = False
        self.out = None
        self.count_videos = 0
        self.last_rec = False
        self.timing = 0

        # Initialize the background subtractor
        self.bg_subtractor = cv2.createBackgroundSubtractorMOG2()

    def __del__(self):
        self.cap.release()

    def get_frame(self):
        first_frame = None  # Initialize a variable to store the first frame

        while True:
            ret, frame = self.cap.read()
            
            if not ret:
                print("Error: Couldn't read a frame from the camera.")
                continue

            frame = cv2.resize(frame, (640, 360))

            # Frame Differencing
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            gray = cv2.GaussianBlur(gray, (21, 21), 0)
            
            if first_frame is None:
                first_frame = gray
                continue

            delta_frame = cv2.absdiff(first_frame, gray)
            _, delta_thresh = cv2.threshold(delta_frame, 25, 255, cv2.THRESH_BINARY)

            # Background Subtraction
            fgmask = self.bg_subtractor.apply(frame)

            # Combine both methods
            combined_mask = cv2.bitwise_or(delta_thresh, fgmask)
            cnts, _ = cv2.findContours(combined_mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            start_rec = False
            for contour in cnts:
                if cv2.contourArea(contour) < 1000:
                    continue
                x, y, w, h = cv2.boundingRect(contour)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 3)
                start_rec = True


            self._handle_recording_status(start_rec)

            ret, jpeg = cv2.imencode('.jpg', frame)
            self._write_frame_to_video(ret, frame)
            return jpeg.tobytes()


    def _handle_recording_status(self, start_rec):
        if start_rec:
            if not self.last_rec:
                self.count_videos += 1
                self.timing = time.time()
            self.is_record = True
            self.last_rec = True
            if time.time() - self.timing > 20.0:
                self.is_record = False
                self.last_rec = False
                self.out = None
        else:
            if self.last_rec:
                self.timing = time.time()
            self.last_rec = False
            if time.time() - self.timing > 3.0:
                self.is_record = False
                self.out = None

   
    def _write_frame_to_video(self, ret, frame):
        if self.is_record:
            if self.out is None:
                fourcc = cv2.VideoWriter_fourcc(*'H264')  # Using H.264 codec
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')  # YYYYMMDD_HHMMSS format
                road = f'./static/videos/video_{timestamp}.mp4'

                self.out = cv2.VideoWriter(road, fourcc, 20.0, (640, 360))
                


            if ret:
                self.out.write(frame)
            else:
                if self.out is not None:
                    self.out.release()
                    self.out = None
        else:
            cv2.destroyAllWindows()

    def start_record(self):
        self.is_record = True
        self.count_videos += 1
        send_email("Danger!!!")

    def stop_record(self):
        self.is_record = False
        if self.out:
            self.out.release()
        self.out = None
