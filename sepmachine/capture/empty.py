from sepmachine.capture.base import BaseCapture


class EmptyCapture(BaseCapture):
    """
    empty capture if you are going to send a video directly
    """

    def cap(self, video_path: str) -> bool:
        return True

