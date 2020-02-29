from sepmachine.handler.base import BaseHandler

from stagesepx.cutter import VideoCutter
from stagesepx.classifier.keras import KerasClassifier
from stagesepx.reporter import Reporter
from stagesepx.video import VideoObject
from loguru import logger


class KerasHandler(BaseHandler):
    def __init__(self, model_path: str = None, *args, **kwargs):
        self.model_path: str = model_path
        super(KerasHandler, self).__init__(*args, **kwargs)

    def handle(self, video_path: str) -> bool:
        super(KerasHandler, self).handle(video_path)
        video = VideoObject(video_path)
        if self.preload:
            video.load_frames()

        # --- cutter ---
        cutter = VideoCutter()
        res = cutter.cut(video)
        stable, unstable = res.get_range(threshold=0.98, offset=3)

        # --- classify ---
        cl = KerasClassifier()
        if self.model_path:
            logger.info("load existed pre-train model")
            cl.load_model(self.model_path)
        else:
            data_home = res.pick_and_save(
                stable, self.frame_count, to_dir=self.result_path
            )
            cl.train(data_home)
        self.classifier_result = cl.classify(video, stable)

        # --- draw ---
        r = Reporter()
        r.draw(self.classifier_result, report_path=self.result_report_path)
        return True
