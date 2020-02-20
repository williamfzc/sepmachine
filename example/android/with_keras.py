from sepmachine.pipeline import BasePipeline
from sepmachine.handler import KerasHandler
from sepmachine.capture import AdbCapture


video_path = "../../demo1.mp4"
model_path = "../../output.h5"

empty_cap = AdbCapture("123456F")
handler = KerasHandler(model_path=model_path)
pipeline = BasePipeline(empty_cap, handler)
pipeline.run(video_path)
