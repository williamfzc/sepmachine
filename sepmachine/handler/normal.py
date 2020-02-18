from sepmachine.handler.base import BaseHandler


class NormalHandler(BaseHandler):
    def handle(self, video_path: str) -> bool:
        return True
