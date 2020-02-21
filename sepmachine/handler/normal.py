from sepmachine.handler.base import BaseHandler

from stagesepx.cutter import VideoCutter
from stagesepx.classifier import SVMClassifier
from stagesepx.reporter import Reporter
from stagesepx.video import VideoObject


class NormalHandler(BaseHandler):
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
        self.classifier_result = cl.classify(video, stable)

        # --- draw ---
        r = Reporter()
        r.draw(self.classifier_result)
        return True
