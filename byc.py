#!/usr/bin/env python3

from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QPushButton, QVBoxLayout, QApplication, QWidget
from picamera2.previews.qt import QGlPicamera2
from picamera2 import Picamera2
from gpiozero import Button, LED, PWMOutputDevice
from libcamera import Transform
import time

hardware_camera = Picamera2()
hardware_camera.configure(hardware_camera.create_preview_configuration(transform=Transform(hflip=1, vflip=1)))
cfg = hardware_camera.create_still_configuration(transform=Transform(hflip=1, vflip=1))

hardware_button = Button(14)
hardware_button_led = LED(18)
vibe = PWMOutputDevice(25)

def on_button_clicked():
  print("acquiring")
  timestr = time.strftime("%Y%m%d-%H%M%S")
  hardware_camera.switch_mode_and_capture_file(cfg, f"/home/justin/Pictures/picam/{timestr}.jpg", signal_function=qpicamera2.signal_done)
  vibe.on()
  time.sleep(0.2)
  vibe.off()
  print(f"done {timestr}")

def capture_done():
  print("ready")

app = QApplication([])
qpicamera2 = QGlPicamera2(hardware_camera, width=800, height=600)

hardware_button.when_pressed = on_button_clicked

window = QWidget()

qpicamera2.done_signal.connect(capture_done)
layout = QVBoxLayout()
layout.setContentsMargins(0, 0, 0, 0)
layout.addWidget(qpicamera2)

window.setWindowTitle("Qt Picamera2 App")
window.setLayout(layout)
window.setCursor(Qt.BlankCursor)   

hardware_camera.start()
window.showFullScreen()
hardware_button_led.on()
vibe.on()
time.sleep(1)
vibe.off()
print("ready")
app.exec()

led.off()
    
