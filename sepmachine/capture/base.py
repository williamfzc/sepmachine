class BaseCapture(object):
    def cap(self, video_path: str) -> bool:
        raise NotImplementedError
