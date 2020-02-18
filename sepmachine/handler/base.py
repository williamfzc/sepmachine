class BaseHandler(object):
    def handle(self, video_path: str) -> bool:
        raise NotImplementedError
