from sepmachine.pipeline import BasePipeline
from sepmachine.capture.adb import AdbCapture
from sepmachine.handler.normal import NormalHandler

import time

video_path = "../../demo1.mp4"


# custom capture
class MyAdbCapture(AdbCapture):
    def operate(self) -> bool:
        # do something??
        time.sleep(10)
        return True


# custom handler
class MyNormalHandler(NormalHandler):
    def handle(self, video_path: str) -> bool:
        handler_result: bool = super(MyNormalHandler, self).handle(video_path)
        assert self.classifier_result

        # do some extra calculations?
        print(self.classifier_result.data)
        return handler_result


adb_cap = MyAdbCapture(serial_no="123456F")
handler = MyNormalHandler()
pipeline = BasePipeline(adb_cap, handler)
pipeline.run(video_path)
