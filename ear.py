# ear.py
import math
from collections import deque

def euclidean(a, b):
    return math.hypot(a[0]-b[0], a[1]-b[1])

def eye_aspect_ratio(eye):
    if len(eye) != 6:
        return 0.0
    A = euclidean(eye[1], eye[5])
    B = euclidean(eye[2], eye[4])
    C = euclidean(eye[0], eye[3])
    return (A + B) / (2.0 * C) if C != 0 else 0.0

class DrowsinessDetector:
    """Tracks average EAR and signals drowsiness after consecutive low EAR frames."""
    def __init__(self, threshold=0.25, consec_frames=15, smoothing=5):
        self.threshold = threshold
        self.consec_frames = consec_frames
        self.counter = 0
        self.drowsy = False
        self.ear_values = deque(maxlen=smoothing)

    def update(self, ear):
        self.ear_values.append(ear)
        avg_ear = sum(self.ear_values) / len(self.ear_values)
        if avg_ear < self.threshold:
            self.counter += 1
        else:
            self.counter = 0
            self.drowsy = False
        if self.counter >= self.consec_frames:
            self.drowsy = True
        return avg_ear, self.drowsy
