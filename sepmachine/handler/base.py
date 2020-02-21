import typing
from loguru import logger
from stagesepx.classifier import ClassifierResult


class BaseHandler(object):
    def __init__(self, preload: bool = None, frame_count: int = None):
        # config here
        self.preload: bool = preload or True
        self.frame_count: int = frame_count or 5
        # result
        self.classifier_result: typing.Optional[ClassifierResult] = None

        logger.info(f"config: {self.__dict__}")

    def handle(self, video_path: str) -> bool:
        raise NotImplementedError
