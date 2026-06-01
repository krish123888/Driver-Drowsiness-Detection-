# gui.py
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import threading, platform, time, cv2, os

# Cross-platform sound support
if platform.system() == "Windows":
    import winsound
else:
    try:
        from playsound import playsound
    except ImportError:
        playsound = None

from capture import VideoStream
from ear import eye_aspect_ratio, DrowsinessDetector

ALARM_PATH = "alarm.wav"   # Optional WAV sound
EAR_THRESHOLD = 0.23
CONSEC_FRAMES = 18

class DrowsyApp:
    def __init__(self, root):
        self.root = root
        root.title("🚗 Drowsiness Detection System")
        root.configure(bg="#111")

        self.vs = VideoStream()
        self.vs.start()
        self.detector = DrowsinessDetector(EAR_THRESHOLD, CONSEC_FRAMES)
        self.alarm_on = False

        # UI layout
        self.canvas = tk.Label(root, bg="#000")
        self.canvas.pack(padx=10, pady=10)

        self.status_var = tk.StringVar(value="Status: Awake")
        self.status_lbl = tk.Label(root, textvariable=self.status_var,
                                   font=("Helvetica", 18, "bold"), bg="#111", fg="lime")
        self.status_lbl.pack(pady=10)

        self.ear_var = tk.StringVar(value="EAR: --")
        tk.Label(root, textvariable=self.ear_var, font=("Helvetica", 16), bg="#111", fg="#00ffcc").pack()

        self.update_frame()
        root.protocol("WM_DELETE_WINDOW", self.on_close)

    # 🔊 Alarm function (cross-platform)
    def play_alarm(self):
        while self.alarm_on:
            if platform.system() == "Windows":
                # Try playing custom WAV file, else beep
                if os.path.exists(ALARM_PATH):
                    winsound.PlaySound(ALARM_PATH, winsound.SND_FILENAME)
                else:
                    winsound.Beep(1000, 800)
            elif playsound is not None and os.path.exists(ALARM_PATH):
                try:
                    playsound(ALARM_PATH)
                except Exception:
                    pass
            time.sleep(0.1)

    def update_frame(self):
        frame, left, right = self.vs.read()
        if frame is not None:
            if left and right:
                ear_left = eye_aspect_ratio(left)
                ear_right = eye_aspect_ratio(right)
                ear, drowsy = self.detector.update((ear_left + ear_right) / 2.0)
                self.ear_var.set(f"EAR: {ear:.3f}")

                if drowsy:
                    self.status_var.set("⚠️ DROWSY! WAKE UP!")
                    self.status_lbl.config(fg="red")
                    if not self.alarm_on:
                        self.alarm_on = True
                        threading.Thread(target=self.play_alarm, daemon=True).start()
                else:
                    self.status_var.set("Status: Awake")
                    self.status_lbl.config(fg="lime")
                    self.alarm_on = False

            # Draw & show video frame
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(rgb)
            imgtk = ImageTk.PhotoImage(image=img)
            self.canvas.imgtk = imgtk
            self.canvas.config(image=imgtk)

        self.root.after(20, self.update_frame)

    def on_close(self):
        self.alarm_on = False
        self.vs.stop()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    DrowsyApp(root)
    root.mainloop()
