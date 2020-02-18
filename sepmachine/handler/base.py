from loguru import logger


class BaseHandler(object):
    def __init__(self, preload: bool = None, frame_count: int = None):
        # config here
        self.preload: bool = preload or True
        self.frame_count: int = frame_count or 5

        logger.info(f"config: {self.__dict__}")

    def handle(self, video_path: str) -> bool:
        raise NotImplementedError
