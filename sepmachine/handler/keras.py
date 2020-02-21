from sepmachine.handler.base import BaseHandler

from stagesepx.cutter import VideoCutter
from stagesepx.classifier.keras import KerasClassifier
from stagesepx.reporter import Reporter
from stagesepx.video import VideoObject
from loguru import logger


class KerasHandler(BaseHandler):
    def __init__(self, model_path: str = None, *args, **kwargs):
        super(KerasHandler, self).__init__(*args, **kwargs)
        self.model_path: str = model_path

    def handle(self, video_path: str) -> bool:
        video = VideoObject(video_path)
        if self.preload:
            video.load_frames()

        # --- cutter ---
        cutter = VideoCutter()
        res = cutter.cut(video)
        stable, unstable = res.get_range()

        # --- classify ---
        cl = KerasClassifier()
        if self.model_path:
            logger.info("load existed pre-train model")
            cl.load_model(self.model_path)
        else:
            data_home = res.pick_and_save(stable, self.frame_count)
            cl.train(data_home)
        self.classifier_result = cl.classify(video, stable)

        # --- draw ---
        r = Reporter()
        r.draw(self.classifier_result)
        return True
