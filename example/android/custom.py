from sepmachine.pipeline import BasePipeline
from sepmachine.capture.adb import AdbCapture
from sepmachine.capture.scrcpy import ScrcpyCapture
from sepmachine.handler.keras import KerasHandler

import uiautomator2 as u2
import time

VIDEO_PATH = "../../demo1.mp4"
WEIXIN_LABEL = "微信"
WEIXIN_LOGIN_LABEL = "登录"
WEIXIN_PACKAGE_NAME = "com.tencent.mm"


# custom capture
class MyScrcpyCapture(ScrcpyCapture):
    def start(self, video_path: str) -> bool:
        self.prepare()
        return super(MyScrcpyCapture, self).start(video_path)

    def prepare(self):
        self.u2_device = u2.connect(self.serial_no)
        self.u2_device.app_clear(WEIXIN_PACKAGE_NAME)
        # make sure env is normal
        assert self.u2_device(text=WEIXIN_LABEL).exists(), "weixin logo not existed"

    def operate(self) -> bool:
        # do something??
        time.sleep(1)
        self.u2_device(text=WEIXIN_LABEL).click()
        while not self.u2_device(text=WEIXIN_LOGIN_LABEL).exists():
            time.sleep(1)
        time.sleep(2)
        return True


# custom handler
class MyKerasHandler(KerasHandler):
    def __init__(self, *args, **kwargs):
        super(MyKerasHandler, self).__init__(*args, **kwargs)

        # you can add custom result handler
        self.result = []

    def handle(self, video_path: str) -> bool:
        handler_result: bool = super(MyKerasHandler, self).handle(video_path)
        assert self.classifier_result

        # do some extra calculations?
        # if you want to know:
        # how long from stage 0 end to stage 2 start?
        end_frame_of_0 = self.classifier_result.last("0")
        start_frame_of_2 = self.classifier_result.first("2")
        cost = start_frame_of_2.timestamp - end_frame_of_0.timestamp
        print(f"stage 0 end: {end_frame_of_0.frame_id, end_frame_of_0.timestamp}")
        print(f"stage 2 start: {start_frame_of_2.frame_id, start_frame_of_2.timestamp}")
        print(f"and the cost: {cost}")

        # or maybe unstable ranges
        unstable_ranges = self.classifier_result.get_not_stable_stage_range()
        first_changing_frame = unstable_ranges[1][0]

        end_time = start_frame_of_2.timestamp
        start_time = first_changing_frame.timestamp
        new_cost = end_time - start_time
        self.result.append([start_time, end_time, new_cost])

        # 0.3.1 +
        # cost = self.time_cost_between("0", "2")

        return handler_result


adb_cap = MyScrcpyCapture()
handler = MyKerasHandler(model_path="output.h5", result_path="./hahaha")
pipeline = BasePipeline(adb_cap, handler)
pipeline.loop_run(loop_num=3)
print(handler.result)
