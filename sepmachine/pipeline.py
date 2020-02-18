from sepmachine.capture.base import BaseCapture
from sepmachine.handler.base import BaseHandler

from loguru import logger


class BasePipeline(object):
    def __init__(self, capture: BaseCapture, handler: BaseHandler):
        self.capture: BaseCapture = capture
        self.handler: BaseHandler = handler

        logger.info(f"capture: {self.capture.__class__}")
        logger.info(f"handler: {self.handler.__class__}")

    def run(self, video_path: str):
        logger.info("start pipeline")
        logger.info(f"video: {video_path}")

        # capture
        self.capture.start(video_path)
        logger.info("start recording")
        self.capture.operate()
        logger.info("stop recording")
        capture_result: bool = self.capture.end()
        assert capture_result

        # handler
        handle_result: bool = self.handler.handle(video_path)
        assert handle_result
        logger.info("end pipeline")
