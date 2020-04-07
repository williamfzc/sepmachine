import typing
import os
from loguru import logger
from stagesepx.classifier import ClassifierResult
from stagesepx import toolbox


class BaseHandler(object):
    def __init__(
        self, preload: bool = None, frame_count: int = None, result_path: str = None
    ):
        # config here
        self.preload: bool = preload or True
        self.frame_count: int = frame_count or 5
        # result
        self.classifier_result: typing.Optional[ClassifierResult] = None
        self.result_path: str = result_path
        self.result_report_path: str = ""
        if not self.result_path:
            self.result_path = toolbox.get_timestamp_str()
        os.makedirs(self.result_path, exist_ok=True)

        # extra args
        self.extras = dict()

        logger.info(f"handler config: {self.__dict__}")

    def handle(self, video_path: str) -> bool:
        self.result_report_path: str = os.path.join(
            self.result_path, f"{toolbox.get_timestamp_str()}.html"
        )
        return True

    def time_cost_between(self, start_stage: str, end_stage: str) -> float:
        return (
            self.classifier_result.last(start_stage).timestamp
            - self.classifier_result.first(end_stage).timestamp
        )
