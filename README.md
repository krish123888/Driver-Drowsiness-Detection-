# Driver Drowsiness Detection System

A real-time drowsiness detection system that uses a webcam and MediaPipe Face Mesh 
to monitor eye openness via the Eye Aspect Ratio (EAR) algorithm. 
When prolonged eye closure is detected, an audio alarm is triggered to alert the driver.

## Features
- Real-time face and eye landmark tracking via MediaPipe
- EAR-based drowsiness detection with smoothing to reduce false positives
- Audio alarm (WAV or system beep) — cross-platform
- Live video feed with EAR display in a Tkinter GUI

## Tech Stack
Python · OpenCV · MediaPipe · Tkinter · Pillow

## How to Run

### 1. Clone the repository
git clone https://github.com/krish123666/Driver-Drowsiness-Detection.git
cd Driver-Drowsiness-Detection

### 2. Install dependencies
pip install -r requirements.txt

### 3. Run
python gui.py

## How it Works
1. Webcam frames are captured in a background thread
2. MediaPipe Face Mesh extracts 6 landmarks per eye
3. EAR is computed each frame — values below ~0.23 indicate closed eyes
4. If EAR stays low for 18+ consecutive frames, drowsiness is flagged and alarm fires

## Project Structure
| File | Purpose |
|------|---------|
| gui.py | Main app — Tkinter UI and alarm logic |
| capture.py | Webcam capture + MediaPipe landmark extraction |
| ear.py | EAR calculation and drowsiness detection logic |
| alarm.wav | Alert sound file |
| requirements.txt | Python dependencies |
