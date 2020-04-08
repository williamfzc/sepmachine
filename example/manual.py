from sepmachine.pipeline import BasePipeline
from sepmachine.capture.scrcpy import ScrcpyManualCapture
from sepmachine.handler.normal import NormalHandler


sc = ScrcpyManualCapture()
handler = NormalHandler()
pipeline = BasePipeline(sc, handler, {"a": "n"})
pipeline.run()
