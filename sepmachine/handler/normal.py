from sepmachine.handler.base import BaseHandler

from stagesepx.cutter import VideoCutter
from stagesepx.classifier import SVMClassifier
from stagesepx.reporter import Reporter
from stagesepx.video import VideoObject
from loguru import logger


class NormalHandler(BaseHandler):
    def __init__(
            self,
            preload: bool = None,
            frame_count: int = None,
    ):
        # config here
        self.preload: bool = preload or True
        self.frame_count: int = frame_count or 5

        logger.info(f"config: {self.__dict__}")

    def handle(self, video_path: str) -> bool:
        video = VideoObject(video_path)
        if self.preload:
            video.load_frames()

        # --- cutter ---
        cutter = VideoCutter()
        res = cutter.cut(video)
        stable, unstable = res.get_range()
        data_home = res.pick_and_save(stable, self.frame_count)

        # --- classify ---
        cl = SVMClassifier()
        cl.load(data_home)
        cl.train()
        classify_result = cl.classify(video, stable)

        # --- draw ---
        r = Reporter()
        r.draw(classify_result)
        return True
