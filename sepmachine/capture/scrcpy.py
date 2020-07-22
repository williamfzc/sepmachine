from sepmachine.capture.base import BaseCapture

import typing
import time
import ffmpeg
import tempfile
import os
import shutil
import subprocess
import signal
import sys
from loguru import logger
from minadb import ADBDevice


class ScrcpyCapture(BaseCapture):
    def __init__(self, serial_no: str = None, fps: int = 60, manual_mode: bool = None):
        super(ScrcpyCapture, self).__init__()
        # args
        self.serial_no: str = serial_no
        self.fps: int = fps

        # others
        self.device: ADBDevice = ADBDevice(self.serial_no)
        self.record_stop: typing.Optional[typing.Callable] = None
        self.record_proc: typing.Optional[subprocess.Popen] = None
        self.video_path: str = ""
        self.temp_video_path: str = ""
        self.manual_mode: bool = bool(manual_mode)
        logger.info(f"config: {self.__dict__}")

    def start(self, video_path: str) -> bool:
        self.video_path = video_path
        # save to temp file (scrcpy will save video on pc side directly)
        temp_video = tempfile.NamedTemporaryFile(mode="wb+", suffix=".mkv")
        temp_video_path = temp_video.name
        self.temp_video_path = temp_video_path
        temp_video.close()
        logger.debug(f"video will be saved to {self.temp_video_path}")

        device_flag = ["-s", self.serial_no] if self.serial_no else []
        record_command = [
            "scrcpy",
            *device_flag,
            "--render-expired-frames",
            # no mirror if in auto mode
            "-Nr" if not self.manual_mode else "-r",
            self.temp_video_path,
        ]
        logger.info(f"trying to start: {record_command}")
        proc = subprocess.Popen(record_command)
        # wait for scrcpy
        time.sleep(5)
        assert proc.poll() is None, f"run command failed: {record_command}"

        def stop():
            if sys.platform == "win32":
                self.device.kill_process_by_name("app_process")
                proc.terminate()
            else:
                proc.send_signal(signal.SIGINT)

        self.record_stop = stop
        self.record_proc = proc
        return True

    def operate(self) -> bool:
        # auto mode
        if not self.manual_mode:
            time.sleep(5)
            return True
        # manual mode, wait until process dead
        while self.record_proc.poll() is None:
            time.sleep(1)
        return True

    def end(self) -> bool:
        assert self.record_stop and self.video_path
        self.record_stop()

        try:
            # ffmpeg converter
            stream = ffmpeg.input(self.temp_video_path)
            stream = ffmpeg.filter(stream, "fps", fps=self.fps)
            stream = ffmpeg.output(stream, self.video_path)
            ffmpeg.run(stream, overwrite_output=True)
            logger.info(f"video convert finished. fps: {self.fps}")
        except FileNotFoundError:
            logger.warning("no ffmpeg installation found, skip fps converter")
            logger.warning("WARNING: ffmpeg is necessary for accuracy")
            shutil.copyfile(self.temp_video_path, self.video_path)
        except ffmpeg._run.Error as e:
            logger.warning(e)
            command = [
                "ffmpeg",
                "-i",
                self.temp_video_path,
                "-r",
                str(self.fps),
                self.video_path,
            ]
            logger.info(f"retry with command line calling: {command}")
            subprocess.check_call(command)
        finally:
            logger.info(f"video has been moved to: {self.video_path}")

        try:
            os.remove(self.temp_video_path)
            logger.debug(f"removed: {self.temp_video_path}")
        except PermissionError as e:
            logger.error(e)
            logger.warning("skip removing temp file")

        return True


class ScrcpyManualCapture(ScrcpyCapture):
    def __init__(self, *args, **kwargs):
        super(ScrcpyManualCapture, self).__init__(*args, **kwargs)
        self.manual_mode = True
