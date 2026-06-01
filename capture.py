# capture.py
import cv2
import mediapipe as mp
import threading

LEFT_EYE = [33, 160, 158, 133, 153, 144]
RIGHT_EYE = [263, 387, 385, 362, 380, 373]
mp_face_mesh = mp.solutions.face_mesh

class VideoStream:
    """Continuously captures frames and extracts face/eye landmarks using MediaPipe."""
    def __init__(self, src=0):
        self.cap = cv2.VideoCapture(src)
        self.running = False
        self.frame = None
        self.left_eye = None
        self.right_eye = None
        self.lock = threading.Lock()
        self.facemesh = mp_face_mesh.FaceMesh(
            max_num_faces=1,
            refine_landmarks=True,
            min_detection_confidence=0.6,
            min_tracking_confidence=0.6
        )

    def start(self):
        if self.running:
            return
        self.running = True
        threading.Thread(target=self._update, daemon=True).start()

    def _update(self):
        while self.running:
            ret, frame = self.cap.read()
            if not ret:
                continue
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = self.facemesh.process(rgb)
            left, right = None, None
            if results.multi_face_landmarks:
                lm = results.multi_face_landmarks[0]
                h, w, _ = frame.shape
                left = [(int(lm.landmark[i].x * w), int(lm.landmark[i].y * h)) for i in LEFT_EYE]
                right = [(int(lm.landmark[i].x * w), int(lm.landmark[i].y * h)) for i in RIGHT_EYE]
            with self.lock:
                self.frame = frame
                self.left_eye = left
                self.right_eye = right

    def read(self):
        """Return latest frame + eye landmarks safely, even before initialization."""
        with self.lock:
            if self.frame is None:
                return None, None, None
            return self.frame.copy(), self.left_eye, self.right_eye

    def stop(self):
        self.running = False
        if self.cap.isOpened():
            self.cap.release()
        self.facemesh.close()
