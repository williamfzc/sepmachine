from sepmachine.capture.base import BaseCapture


class EmptyCapture(BaseCapture):
    """
    empty capture if you are going to send a video directly
    """

    def start(self, video_path: str) -> bool:
        return True

    def operate(self) -> bool:
        return True

    def end(self) -> bool:
        return True
