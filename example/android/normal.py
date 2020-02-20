from sepmachine.pipeline import BasePipeline
from sepmachine.capture.adb import AdbCapture
from sepmachine.handler.normal import NormalHandler


video_path = "../../demo1.mp4"

adb_cap = AdbCapture(serial_no="123456F")
handler = NormalHandler()
pipeline = BasePipeline(adb_cap, handler)
pipeline.run(video_path)
