from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QPushButton, QVBoxLayout, QApplication, QWidget
from picamera2.previews.qt import QGlPicamera2
from picamera2 import Picamera2
from gpiozero import Button, LED, PWMOutputDevice
from libcamera import Transform
import time

picam2 = Picamera2()
picam2.configure(picam2.create_preview_configuration(transform=Transform(hflip=1, vflip=1)))
cfg = picam2.create_still_configuration(transform=Transform(hflip=1, vflip=1))

hardware_button = Button(14)
led = LED(18)
vibe = PWMOutputDevice(25)

def on_button_clicked():
  button.setEnabled(False)
  
  print("acquiring")
  timestr = time.strftime("%Y%m%d-%H%M%S")
  picam2.switch_mode_and_capture_file(cfg, f"/home/justin/Pictures/picam/{timestr}.jpg", signal_function=qpicamera2.signal_done)
  vibe.on()
  time.sleep(0.2)
  vibe.off()
  print(f"done {timestr}")
  
def capture_done():
  picam2.wait()
  button.setEnabled(True)
  print("ready")
  
def trigger():
    button.click()

app = QApplication([])
qpicamera2 = QGlPicamera2(picam2, width=800, height=600)
button = QPushButton()
hardware_button.when_pressed = trigger

window = QWidget()

qpicamera2.done_signal.connect(capture_done)
button.clicked.connect(on_button_clicked)
layout = QVBoxLayout()
layout.setContentsMargins(0, 0, 0, 0)
layout.addWidget(qpicamera2)
#layout_v.addWidget(button)
window.setWindowTitle("Qt Picamera2 App")
window.setLayout(layout)
window.setCursor(Qt.BlankCursor)   

picam2.start()
window.showFullScreen()
led.on()
vibe.on()
time.sleep(1)
vibe.off()
print("ready")
app.exec()

led.off()
    
