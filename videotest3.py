from picamera2 import Picamera2, Preview
from picamera2.encoders import H264Encoder
from picamera2.outputs import FfmpegOutput
import time

picam2 = Picamera2()
config = picam2.create_video_configuration()
picam2.configure(config)
picam2.start_preview(Preview.QTGL, width=800, height = 600)
picam2.start()

encoder = H264Encoder(1000000)
encoder.output = FfmpegOutput("test1.mp4")
picam2.start_encoder(encoder)
time.sleep(5)
picam2.stop_encoder()

encoder.output = FfmpegOutput("test2.mp4")
picam2.start_encoder(encoder)
time.sleep(5)
picam2.stop_encoder()

picam2.stop()