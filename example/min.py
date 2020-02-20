from sepmachine.pipeline import BasePipeline
from sepmachine.capture.empty import EmptyCapture
from sepmachine.handler.normal import NormalHandler


video_path = "../demo.mp4"

empty_cap = EmptyCapture()
handler = NormalHandler()
pipeline = BasePipeline(empty_cap, handler)
pipeline.run(video_path)
