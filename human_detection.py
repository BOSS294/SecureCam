import cv2
import datetime
import pyttsx3
import time
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QWidget, QTextEdit
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import QThread, pyqtSignal

# Initialize text-to-speech engine
engine = pyttsx3.init()

# Load pre-trained model for human detection
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Initialize flags for tracking recording status and detection
recording = False
video_writer = None
record_start_time = None
last_face_detected_time = time.time()

# Define a fixed square box for human detection
box_x, box_y = 200, 150  # Position of the top-left corner of the box
box_size = 200  # Size of the square box
max_recording_duration = 10 * 60  # 10 minutes in seconds

class VideoThread(QThread):
    change_pixmap_signal = pyqtSignal(QImage)

    def run(self):
        global recording, video_writer, record_start_time, last_face_detected_time

        cap = cv2.VideoCapture(0)
        cap.set(cv2.CAP_PROP_FPS, 30)  # Set FPS to 30 for normal speed

        while True:
            start_time = time.time()
            ret, frame = cap.read()

            if not ret:
                break

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, 1.1, 4)

            cv2.rectangle(frame, (box_x, box_y), (box_x + box_size, box_y + box_size), (0, 255, 0), 2)
            face_in_box = False

            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
                if is_face_in_box(x, y, w, h, box_x, box_y, box_size):
                    face_in_box = True
                    last_face_detected_time = time.time()

            if face_in_box:
                if not recording:
                    record_start_time = time.time()
                    date_time = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                    start_recording(frame, date_time)
                    recording = True

                if recording and video_writer is not None:
                    end_time = time.time()
                    elapsed_time = end_time - record_start_time
                    if elapsed_time > max_recording_duration:
                        stop_recording()
                        recording = False
                    else:
                        fps = 1 / (end_time - start_time)
                        display_overlay(frame, fps)
                        video_writer.write(frame)

            else:
                if recording and (time.time() - last_face_detected_time) > 20:
                    stop_recording()
                    recording = False

            end_time = time.time()
            fps = 1 / (end_time - start_time)
            display_overlay(frame, fps)

            rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h, w, ch = rgb_image.shape
            bytes_per_line = ch * w
            q_img = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
            self.change_pixmap_signal.emit(q_img)

        cap.release()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Camera Monitoring System')
        self.setGeometry(100, 100, 1200, 800)  # Adjusted to provide more space

        self.create_widgets()
        self.create_layout()
        self.create_connections()

        self.video_thread = VideoThread()
        self.video_thread.change_pixmap_signal.connect(self.update_image)
        self.video_thread.start()

        self.update_info()

    def create_widgets(self):
        self.camera_label = QLabel()
        self.info_text = QTextEdit()
        self.info_text.setReadOnly(True)
        self.info_text.setStyleSheet("color: white; background-color: black;")

        self.view_recordings_btn = QPushButton('View Recordings')
        self.delete_recordings_btn = QPushButton('Delete Recordings')
        self.view_logs_btn = QPushButton('View Logs')
        self.stop_recording_btn = QPushButton('Stop Recording')
        self.stop_alert_btn = QPushButton('Stop Alert')

        self.logs_text = QTextEdit()
        self.logs_text.setReadOnly(True)
        self.logs_text.setStyleSheet("color: green; background-color: black;")

        self.update_logs("System initialized.")

        # Button Styles
        self.stop_recording_btn.setStyleSheet("""
            QPushButton {
                background-color: red;
                color: white;
                border-radius: 15px;
                padding: 10px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: darkred;
            }
        """)

    def create_layout(self):
        info_layout = QVBoxLayout()
        info_layout.addWidget(QLabel('Info'))
        info_layout.addWidget(self.info_text)

        button_layout = QVBoxLayout()
        button_layout.addWidget(self.view_recordings_btn)
        button_layout.addWidget(self.delete_recordings_btn)
        button_layout.addWidget(self.view_logs_btn)
        button_layout.addWidget(self.stop_recording_btn)
        button_layout.addWidget(self.stop_alert_btn)

        logs_layout = QVBoxLayout()
        logs_layout.addWidget(QLabel('Logs'))
        logs_layout.addWidget(self.logs_text)

        right_layout = QVBoxLayout()
        right_layout.addLayout(info_layout)
        right_layout.addLayout(button_layout)
        right_layout.addLayout(logs_layout)

        main_layout = QHBoxLayout()
        main_layout.addWidget(self.camera_label, 3)  # Takes up more space
        main_layout.addLayout(right_layout, 1)  # Right side takes up less space

        container = QWidget()
        container.setLayout(main_layout)
        container.setStyleSheet("background-color: black;")
        self.setCentralWidget(container)

    def create_connections(self):
        self.stop_recording_btn.clicked.connect(self.stop_recording)
        self.view_recordings_btn.clicked.connect(self.view_recordings)
        self.view_logs_btn.clicked.connect(self.view_logs)
        self.stop_alert_btn.clicked.connect(self.stop_alert)

    def update_image(self, q_img):
        self.camera_label.setPixmap(QPixmap.fromImage(q_img))

    def update_info(self):
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.info_text.setText(f"Date: {now}\nTime: {now}\nPlace: Mayank's Room\nLast Human Detected: {now}")

    def stop_recording(self):
        global recording
        if recording:
            stop_recording()
            recording = False
            self.update_info()
            self.update_logs("Recording stopped.")

    def view_recordings(self):
        # Placeholder for view recordings functionality
        self.update_logs("View recordings button clicked.")

    def view_logs(self):
        # Display current logs
        self.update_logs("View logs button clicked.")

    def stop_alert(self):
        # Implement stopping alert functionality
        self.update_logs("Stop alert button clicked.")

    def update_logs(self, message):
        current_logs = self.logs_text.toPlainText()
        new_log_entry = f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {message}\n"
        self.logs_text.setText(current_logs + new_log_entry)

def is_face_in_box(x, y, w, h, box_x, box_y, box_size):
    return (x >= box_x and y >= box_y and (x + w) <= (box_x + box_size) and (y + h) <= (box_y + box_size))

def start_recording(frame, date_time):
    global video_writer
    height, width, _ = frame.shape
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    video_name = f"recorded_{date_time}.avi"
    video_writer = cv2.VideoWriter(video_name, fourcc, 30.0, (width, height))  # Set FPS to 30 for normal speed
    engine.say("Recording started. Human detected inside the box.")
    engine.runAndWait()
    print("Started recording:", video_name)

def stop_recording():
    global video_writer
    if video_writer is not None:
        video_writer.release()
        engine.say("Recording stopped. Human disappeared or maximum duration reached.")
        engine.runAndWait()
        print("Stopped recording.")
        video_writer = None

def display_overlay(frame, fps):
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    font = cv2.FONT_HERSHEY_SIMPLEX
    position_time = (10, 30)
    position_fps = (10, 70)
    font_scale = 0.7
    color = (0, 255, 0)
    thickness = 2

    cv2.putText(frame, f'Time: {current_time}', position_time, font, font_scale, color, thickness, cv2.LINE_AA)
    cv2.putText(frame, f'FPS: {fps:.2f}', position_fps, font, font_scale, color, thickness, cv2.LINE_AA)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
