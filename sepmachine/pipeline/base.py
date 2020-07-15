from sepmachine.capture.base import BaseCapture
from sepmachine.handler.base import BaseHandler

import typing
import tempfile
import os
import time
from loguru import logger


class BasePipeline(object):
    def __init__(self, capture: BaseCapture, handler: BaseHandler, extras: dict = None):
        self.capture: BaseCapture = capture
        self.handler: BaseHandler = handler

        # bind extra args
        self.extras: dict = extras
        self.capture.extras = extras
        self.handler.extras = extras

        logger.info(f"capture: {self.capture.__class__}")
        logger.info(f"handler: {self.handler.__class__}")
        logger.info(f"extras: {self.extras}")

    def run(self, video_path: str = None) -> bool:
        start_time = time.time()
        use_temp: bool = False
        if not video_path:
            logger.info("no specific video path, use temp file")
            use_temp = True
            video_path = tempfile.NamedTemporaryFile(suffix=".mp4", delete=False).name

        try:
            logger.info("start pipeline")
            logger.info(f"video: {video_path}")

            # capture
            self.capture.start(video_path)
            logger.info("start recording")
            self.capture.operate()
            logger.info("stop recording")
            capture_result: bool = self.capture.end()
            assert capture_result, "capture error"

            # handler
            handle_result: bool = self.handler.handle(video_path)
            assert handle_result, "handler error"
            logger.info("end pipeline")
            return True
        except Exception as e:
            logger.exception(e)
            return False
        finally:
            if use_temp:
                try:
                    logger.debug(f"remove tempfile: {video_path}")
                    os.remove(video_path)
                # windows issue
                except PermissionError as e:
                    logger.error(e)
            end_time = time.time()
            cost = end_time - start_time
            logger.info(f"time cost: {cost}")

    def loop_run(self, video_path: str = None, loop_num: int = 1) -> typing.List[bool]:
        ret_list = list()
        for index in range(loop_num):
            logger.info(f"loop: {index}")
            ret = self.run(video_path)
            ret_list.append(ret)
        return ret_list
