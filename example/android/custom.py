from sepmachine.pipeline import BasePipeline
from sepmachine.capture.adb import AdbCapture
from sepmachine.handler.keras import KerasHandler

import uiautomator2 as u2
import time

VIDEO_PATH = "../../demo1.mp4"
WEIXIN_LABEL = "微信"
WEIXIN_PACKAGE_NAME = "com.tencent.mm"


# custom capture
class MyAdbCapture(AdbCapture):
    def __init__(self, *args, **kwargs):
        super(MyAdbCapture, self).__init__(*args, **kwargs)
        self.prepare()

    def prepare(self):
        self.u2_device = u2.connect(self.serial_no)
        self.u2_device.app_clear(WEIXIN_PACKAGE_NAME)
        self.device.kill_process_by_name("screenrecord")
        # make sure env is normal
        assert self.u2_device(text=WEIXIN_LABEL).exists()

    def operate(self) -> bool:
        # do something??
        time.sleep(2)
        self.u2_device(text=WEIXIN_LABEL).click()
        time.sleep(4)
        return True


# custom handler
class MyKerasHandler(KerasHandler):
    def handle(self, video_path: str) -> bool:
        handler_result: bool = super(MyKerasHandler, self).handle(video_path)
        assert self.classifier_result

        # do some extra calculations?
        # if you want to know:
        # how long from stage 0 end to stage 1 start?
        end_frame_of_0 = self.classifier_result.last("0")
        start_frame_of_1 = self.classifier_result.first("1")
        cost = start_frame_of_1.timestamp - end_frame_of_0.timestamp
        print(f"stage 0 end: {end_frame_of_0.frame_id, end_frame_of_0.timestamp}")
        print(f"stage 1 start: {start_frame_of_1.frame_id, start_frame_of_1.timestamp}")
        print(f"and the cost: {cost}")

        return handler_result


adb_cap = MyAdbCapture(serial_no="9c12aa96")
handler = MyKerasHandler(model_path="./output.h5")
pipeline = BasePipeline(adb_cap, handler)
pipeline.run(VIDEO_PATH)
