class BaseCapture(object):
    def start(self, video_path: str) -> bool:
        raise NotImplementedError

    def operate(self) -> bool:
        raise NotImplementedError

    def end(self) -> bool:
        raise NotImplementedError
