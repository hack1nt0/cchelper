import logging, os
import traceback
import sys
from datetime import datetime

from PySide6.QtCore import *
from PySide6.QtWidgets import *
from PySide6.QtGui import *
import cchelper.paths as paths


class Logger:
    def __init__(self) -> None:
        self.logger = logging.getLogger("CcHelper")
        self.logger.setLevel(logging.DEBUG)
        # self.log_level = logging.INFO
        # logging.basicConfig(
        #     filename=get_log_fn(),
        #     filemode="w",
        #     format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        #     level=self.log_level,
        # )
        file_h = logging.FileHandler(paths.data("cchelper.log"))
        file_h.setFormatter(
            logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        )
        file_h.setLevel(logging.DEBUG)
        self.logger.addHandler(file_h)

        console = logging.StreamHandler()
        console.setLevel(logging.DEBUG)
        console.setFormatter(
            logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        )
        self.logger.addHandler(console)

        self.status_bar: QStatusBar = None
        self.font_metrics: QFontMetrics = None

    def set_level(self, v):
        self.logger.setLevel(v)

    def elide_text(self, s: str):
        if self.font_metrics is None:
            self.font_metrics = QFontMetrics(self.status_bar.font())
        return self.font_metrics.elidedText(s, Qt.TextElideMode.ElideMiddle, 600)

    def error(self, msg: str, timeout: int = -1):
        msg = str(msg)
        self.logger.error(msg)
        if self.status_bar:
            self.status_bar.setStyleSheet("color : red")
            msg = " @ ".join((msg, str(datetime.now())))
            self.status_bar.showMessage(self.elide_text(msg), timeout=timeout)

    def info(self, msg: str, timeout=-1):
        msg = str(msg)
        self.logger.info(msg)
        if self.status_bar:
            self.status_bar.setStyleSheet("color : blue")
            msg = " @ ".join((msg, str(datetime.now())))
            self.status_bar.showMessage(self.elide_text(msg), timeout=timeout)

    def warn(self, msg: str, timeout=-1):
        msg = str(msg)
        self.logger.warn(msg)
        if self.status_bar:
            self.status_bar.setStyleSheet("color : yellow")
            msg = " @ ".join((msg, str(datetime.now())))
            self.status_bar.showMessage(self.elide_text(msg), timeout=timeout)

    def exception(self, e: BaseException):
        self.logger.exception(e)

    def debug(self, msg: str):
        msg = str(msg)
        self.logger.debug(msg)


logger = Logger()


def excepthook(exc_type, exc_value, exc_tb):
    tb = "".join(traceback.format_exception(exc_type, exc_value, exc_tb))
    logger.exception(tb)


sys.excepthook = excepthook
