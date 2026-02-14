import cv2
import threading
import time
import config

class CameraFeed:
    def __init__(self, src=config.CAMERA_ID):
        print(f"Connecting to camera: {src} ...")
        self.stream = cv2.VideoCapture(src)
        if not self.stream.isOpened():
            print("ERROR: Could not open camera source.")
        else:
            print("Camera source opened successfully.")
            
        self.stream.set(cv2.CAP_PROP_FRAME_WIDTH, config.FRAME_WIDTH)
        self.stream.set(cv2.CAP_PROP_FRAME_HEIGHT, config.FRAME_HEIGHT)
        (self.grabbed, self.frame) = self.stream.read()
        if not self.grabbed:
            print("WARNING: Initial frame read failed.")
        
        self.stopped = False
        self.lock = threading.Lock()

    def start(self):
        t = threading.Thread(target=self.update, args=())
        t.daemon = True
        t.start()
        return self

    def update(self):
        while True:
            if self.stopped:
                return
            
            (grabbed, frame) = self.stream.read()
            with self.lock:
                self.grabbed = grabbed
                self.frame = frame
            time.sleep(0.01) # Small sleep to prevent tight loop burning CPU

    def read(self):
        with self.lock:
            return self.frame.copy() if self.frame is not None else None

    def stop(self):
        self.stopped = True
        self.stream.release()
